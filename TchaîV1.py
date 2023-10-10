from flask import Flask, request 
from flask_cors import CORS
import sys
import csv
import os

app = Flask(__name__)
app.secret_key = 'We_Like_Tchaî_To_Go_To_Gym'
CORS(app, resources={r"/*": {"origins": "*"}})

transaction = []
file = "transactions.csv"

@app.route('/transaction-<a>-<b>-<amount>', methods=['GET'])
def transaction(a,b,amount):
    if not os.path.exists(file):
        createFile = open(file, "w")
        createFile.close()
    with open(file, "a", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow([a,b,amount])
    return "Transaction successful, " + str(a) + " sent " + str(amount) + " to " + str(b) + "!"

@app.route('/history', methods=["GET"])
def history():
	if os.path.exists(file):
		txt = ""
		with open(file,'r',newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=';')
			for i, line in enumerate(reader):
				txt += str(line) + "\n"
		return txt
	return ""

if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == "check_syntax":
			print("Build [ OK ]")
			exit(0)
		else:
			print("Passed argument not supported ! Supported argument : check_syntax")
			exit(1)
	app.run(debug=True)