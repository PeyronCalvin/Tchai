from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import sys
from datetime import datetime

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
user.flushdb()
transactionRedis.flushdb()

@app.route('/register-<name>', methods=['POST'])
def register(name):
    name = str(name)

    try:
        # Retrieve the current user ID from the Redis database
        id_user = int(user.get('id') or 0)

        # Update the user data in the database
        user.set('id', id_user + 1)
        user.set('name', name)
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

        return jsonify(data)  # Move this line outside the loop
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
                transactionRedis.set(transaction_key, transaction_data)
                
                usera_name = user.get('name' + str(user_a_id))
                userb_name = user.get('name' + str(user_b_id))

                return f"Transaction successful. User {usera_name} sent {amount} to User {userb_name}!"
            else:
                return "Not enough money for transaction."
        else:
            return "At least one user does not exist."
    except Exception as e:
        print(f"Error during transaction: {str(e)}")
        return 'An error occurred during the transaction.'




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