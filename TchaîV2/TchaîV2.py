from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import sys
from datetime import datetime
from hashlib import sha256

app = Flask(__name__)
app.secret_key = 'We_Like_Tchaî_To_Go_To_Gym'
CORS(app, resources={r"/*": {"origins": "*"}})

id_user=0
id_transaction=0
user = redis.Redis(
	host='172.17.0.1',
	port=6379,
	db=0,
	decode_responses=True
)

transactionRedis = redis.Redis(
	host='172.17.0.1',
	port=6379,
	db=1,
	decode_responses=True
)
#Decomment the following line if you want to reset the database
#user.flushdb()
#transactionRedis.flushdb()

@app.route('/register-<name>', methods=['POST'])
def register(name):
    name = str(name)
    
    try:
        # Retrieve the current user ID from the Redis database
        id_user = int(user.get('id') or 0)
        
        # Update the user data in the database
        user.set('id', id_user + 1)
        user.set('name'+ str(id_user), name)
        user.set('balance' + str(id_user), 1000)

        return 'Registration successful!'
    except Exception as e:
        # Log the error for troubleshooting
        print(f"Error during registration: {str(e)}")
        return 'An error occurred during registration.'

@app.route('/users', methods=['GET'])
def showUsers():
    try:
        keys = user.keys("name*")
        data = {}

        for key in keys:
            user_id = key.split('name')[-1]
            name = user.get(key)
            balance = str(user.get('balance' + user_id))
            data[user_id] = {'name': name, 'balance': balance}

        return jsonify(data) 
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    


@app.route('/user-<int:a>', methods=['GET'])
def showUser(a):
    try:
        user_id = str(a)
        name = user.get('name' + user_id)
        balance = user.get('balance' + user_id)

        if name is not None and balance is not None:
            data = {'name': name, 'balance': balance}
            return jsonify({user_id: data})
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    


@app.route('/transaction-<int:a>-<int:b>-<int:amount>', methods=['POST'])
def transaction(a, b, amount):
    try:
        user_a_id = str(a)
        user_b_id = str(b)

        # Check if both users exist in the database
        if user.exists('name' + user_a_id) and user.exists('name' + user_b_id):
            user_a_balance = int(user.get('balance' + user_a_id) or 0)
            user_b_balance = int(user.get('balance' + user_b_id) or 0)

            # Check if user_a has enough balance for the transaction
            if user_a_balance >= amount:
                # Update user balances after successful transaction
                user.set('balance' + user_a_id, user_a_balance - amount)
                user.set('balance' + user_b_id, user_b_balance + amount)

                # Record transaction details in the 'transaction' Redis database
                timestamp = datetime.now().timestamp()
                transaction_key = f"transaction_{timestamp}"
                transaction_data = f"{user_a_id} {user_b_id} {amount} {timestamp}"

                # Create a hash for the transaction tuple (P1, P2, t, a)
                transaction_tuple = f"({user_a_id},{user_b_id},{timestamp},{amount})"
                transaction_hash = sha256(transaction_tuple.encode()).hexdigest()

                # Append the hash to the transaction data
                transaction_data_with_hash = f"{transaction_data} {transaction_hash}"

                # Set the transaction data in Redis
                transactionRedis.set(transaction_key, transaction_data_with_hash)

                return f"Transaction successful. User {user_a_id} sent {amount} to User {user_b_id}!"
            else:
                return "Not enough money for transaction."
        else:
            return "At least one user does not exist."
    except Exception as e:
        print(f"Error during transaction: {str(e)}")
        return 'An error occurred during the transaction.'

@app.route('/verify-integrity', methods=['GET'])
def verify_integrity():
    try:
        keys = sorted(transactionRedis.keys('transaction_*'))
        integrity_check_result = {}

        for key in keys:
            transaction_data = transactionRedis.get(key)
            parts = transaction_data.split(' ')

            if parts:
                # Extracting the stored hash from the transaction data
                stored_hash = parts[4]

                # Extracting P1, P2, t, and a from the transaction details
                user_a_id = parts[0]
                user_b_id = parts[1]
                amount = parts[2]
                timestamp = parts[3]

                # Reconstructing the original tuple for hashing
                transaction_tuple = f"({user_a_id},{user_b_id},{timestamp},{amount})"
                
                # Recalculate the hash based on the reconstructed tuple
                recalculated_hash = sha256(transaction_tuple.encode()).hexdigest()

                # Compare recalculated hash with stored hash
                if recalculated_hash == stored_hash:
                    integrity_check_result[key] = "Integrity verified: Hashes match"
                else:
                    integrity_check_result[key] = "Integrity check failed: Hash mismatch"

        return jsonify(integrity_check_result)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/history', methods=["GET"])
def history():
    try:
        keys = sorted(transactionRedis.keys('*'), key=lambda x: float(x.split('_')[-1]))
        lines = []

        for key in keys:
            lines.append(transactionRedis.get(key))

        return jsonify(lines)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/history-<int:a>', methods=["GET"])
def historyOf(a):
    try:
        user_id = str(a)

        # Retrieve all transaction keys from the database
        keys = transactionRedis.keys('transaction_*')

        # Filter transactions for the specified user
        user_transactions = [
            transactionRedis.get(key) for key in keys if user_id in transactionRedis.get(key)
        ]

        return jsonify(user_transactions)
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == "check_syntax":
			print("Build [ OK ]")
			exit(0)
		else:
			print("Passed argument not supported ! Supported argument : check_syntax")
			exit(1)
	app.run(debug=True)
