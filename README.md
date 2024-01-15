
# TchaîV4 - Cryptographic chaining

## TchaîV4.py

### Functions

- register: 
  - parameters: name (user's name)
  - how it works: create a new user inside redis database, this user will be defined by an id, a name and a balance. The id is unique and is increased by 1 for each user registered. And stores the public key if there is one
  - errors: errors during registration are treated and will appear in the console logs.

- showUsers:
  - how it works: return a json composed of each user under a json format. The key which defined each user is its id and the values are the name and the balance.
  - errors: errors while retrieving users are treated and will appear in the console logs.

-showUser:
  - parameters: a (user's id)
  -how it works: search among all users the values linked with the id provided and return a json of this user.
  - errors: errors while retrieving the specified user are treated and will appear in the console logs.

- transaction:
  - parameters: a (id of the user who sends money), b (id of the user who receives money), amount (amount of the transaction), signature (digital signature to authenticate the transaction)
  - how it works: in a first time, users' existence is checked, then sender's balance is check to verify there is enough money on the account. After this, users' balance are modified and we create a hash using users' ids, the amount of transaction, timestamp and if previous transactions were created we also use the previous hash produced. The transaction is then stored in the database under this form : {user_a_id} {user_b_id} {amount} {timestamp} {hash}.
  - so we check before storing the transaction and thus accepting it. To do this, we use the "is_authentication_verified" function, which returns true if the signature corresponds to the transaction.
  - errors: errors while creating a transaction are treated and will appear in the console logs.

- verify_integrity:
  - how it works: in a first time, every transaction is retrieved, then we retrieve all the values of each transaction, these values are then used to calculate the hash of the transaction. For the first transaction, only users' ids, the amount of transaction and the timestamp will be used to calculate the hash, for the other ones, the previous hash will also be used. This hash is then compared with the stored one. If it is equal then the function returns True, else it returns False.
  - errors: errors while retrieving transactions are treated and will appear in the console logs.

- history: 
  - how it works: every transaction is retrievied and a json of all transactions is returned, it is automatically sorted in a chronological order
  - errors: errors while retrieving transacions are treated and will appear in the console logs. 

- historyOf:
  - parameters: a (user's id)
  - how it works: retrieve every transaction made by a user under a json format, it is automatically sorted in a chronological order.
  - errors: errors while retrieving transacions are treated and will appear in the console logs.

- is_authentication_verified:
  - parameters: public_key (user's public key), message (transaction message containing the two users and the transaction amount), signature (digital signature to authenticate the transaction)
  - how it works: uses the verify method of the public_key object to verify the signature and returns true if the method worked otherwise returns false.




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

### Transaction_secure.py
This code simulates a financial transaction between two users, 'user_a' and 'user_b', using RSA keys for digital signature. It then communicates with the remote server to register the users and the execution of the transaction with curl commands, using the digital signature created from the public keys at the beginning of the code. Finally, the transaction response is printed to check that the transaction has been successful.
