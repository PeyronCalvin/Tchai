
# TchaîV2 - A lightly secured server

## TchaîV2.py

### Functions

- register: 
  - parameters: name (user's name)
  - how it works: create a new user inside redis database, this user will be defined by an id, a name and a balance. The id is unique and is increased by 1 for each user registered. 
  - errors: errors during registration are treated and will appear in the console logs.

- showUsers:
  - how it works: return a json composed of each user under a json format. The key which defined each user is its id and the values are the name and the balance.
  - errors: errors while retrieving users are treated and will appear in the console logs.

-showUser:
  - parameters: a (user's id)
  -how it works: search among all users the values linked with the id provided and return a json of this user.
  - errors: errors while retrieving the specified user are treated and will appear in the console logs.

- transaction:
  - parameters: a (id of the user who sends money), b (id of the user who receives money), amount (amount of the transaction)
  - how it works: in a first time, users' existence is checked, then sender's balance is check to verify there is enough money on the account. After this, users' balance are modified and we create a hash using users' ids, the amount of transaction and timestamp. The transaction is then stored in the database under this form : {user_a_id} {user_b_id} {amount} {timestamp} {hash}.
  - errors: errors while creating a transaction are treated and will appear in the console logs.

- verify_integrity:
  - how it works: in a first time, every transaction is retrieved, then we retrieve all the values of each transaction, these values are then used to calculate the hash of the transaction. This hash is then compared with the stored one. If it is equal then the function returns True, else it returns False.
  - errors: errors while retrieving transactions are treated and will appear in the console logs.

- history: 
  - how it works: every transaction is retrievied and a json of all transactions is returned, it is automatically sorted in a chronological order
  - errors: errors while retrieving transacions are treated and will appear in the console logs. 

- historyOf:
  - parameters: a (user's id)
  - how it works: retrieve every transaction made by a user under a json format, it is automatically sorted in a chronological order.
  - errors: errors while retrieving transacions are treated and will appear in the console logs. 


### Routes

- /register-<name>
  - call register function using the name parameters

- /users
  - call showUsers function

- /user-\<int:a>
  - call showUser function using the a parameter which represent the user's id

- /transaction-\<int:a>-\<int:b>-\<int:amount>
  - call transaction function using the a, b and amount parameters which represent the users' ids and the amount of transaction

- /verify-integrity
  - call verify_integrity function

- /history
  - call history function

- /history-\<int:a>
  - call historyOf function using the a parameter which represents the user's id

### Examples of curl user

```
curl -X POST 127.0.0.1:5000/register-sender
curl -X POST 127.0.0.1:5000/register-FirstReceiver
curl -X POST 127.0.0.1:5000/register-SecondReceiver
curl -X GET 127.0.0.1:5000/users
curl -X GET 127.0.0.1:5000/user-0
curl -X POST 127.0.0.1:5000/transaction-0-1-100
curl -X POST 127.0.0.1:5000/transaction-0-2-200
curl -X GET 127.0.0.1:5000/history
curl -X GET 127.0.0.1:5000/history-2
```

### Attack_TchaîV1.py

This attack won't work anymore, we can check it by following the protocol on TchaîV1 and making a curl on the verify-integrity route. We can see mismatching on transactions.

### Attack_TchaîV2.py

The concept of this attack is easily understandable, the goal is to delete a transaction to set it at 0. In order to do so, we suppose someone has access to the database, this person retrieves all the keys link to the transactions and delete the first transaction.

In order to run the code, you just need to have the server and redis dockers up. You need also to have already created a few transactions to test it. When it's done, you just have to run the code.

_Nota bene: if the server has only one transaction stored, this attack will work, we need to have at least two transactions in the database._
