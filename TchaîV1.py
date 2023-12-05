from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import redis
import sys
import csv
import os

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

transaction = redis.Redis(
	host='172.17.0.1',
	port=6379,
	db=1,
	decode_responses=True
)
#Decomment the following line if you want to reset the database
user.flushdb()
transaction.flushdb()

@app.route('/register-<name>', methods=['GET','POST'])
def register(name):
    name = str(name)

    try:
        # Retrieve the current user ID from the Redis database
        id_user = int(user.get('id') or 0)

        # Check if the user name is already taken
        if user.sismember('nameAlreadyTaken', name):
            return 'Registration is not possible with this name, choose another one.'

        # Update the user data in the database
        user.sadd('nameAlreadyTaken', name)
        user.set('id', id_user + 1)
        user.set('name' + str(id_user), name)
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
            if key != 'nameAlreadyTaken':
                user_id = key.split('name')[-1]
                name = user.get(key)
                balance = str(user.get('balance' + user_id))
                data[user_id] = {'name': name, 'balance': balance}

        return jsonify(data)  # Move this line outside the loop
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/transaction-<a>-<b>-<amount>', methods=['GET'])
def transaction(a,b,amount):
	user_a = request.args[a]
	user_b = request.args[b]
	if user_a!=None and user_b!= None:
		if user_a['balance']>amount:
			user_a['balance'] -= amount
			user_b['balance'] += amount
			return "Transaction successful, " + str(a) + " sent " + str(amount) + " to " + str(b) + "!"
		return "Not enough money for transaction"
	return "At least one user does not exist"

@app.route('/history', methods=["GET"])
def history():
	keys = transaction.keys('*')
	lines = []
	for key in keys:
		lines.append(redis.get(key))
	return transaction #### VERIFIER QUE CA MARCHE

@app.route('/history-<a>', methods=['GET'])
def historyOf(a):
	if os.path.exists(file):
		txt = ""
		with open(file,'r',newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=";")
			for i, line in enumerate(reader):
				if line[0]==str(a) or line[1]==str(a):
					txt+= str(line)+"\n"
			return txt
	return "No file"	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == "check_syntax":
			print("Build [ OK ]")
			exit(0)
		else:
			print("Passed argument not supported ! Supported argument : check_syntax")
			exit(1)
	app.run(debug=True)