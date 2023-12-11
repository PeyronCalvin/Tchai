import redis
from datetime import datetime
from hashlib import sha256

transactionRedis = redis.Redis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=True
)

# Use scan_iter to find keys matching the pattern
timestamp = datetime.now().timestamp()
transaction_key = f"transaction_{timestamp}"
transaction_data = f"0 1 100 {timestamp}"
previous_hash = transactionRedis.get('hash')
if previous_hash:
    transaction_tuple = f"(0,1,{timestamp},100,{previous_hash})"
else:
    transaction_tuple = f"(0,1,{timestamp},100)"
transaction_hash = sha256(transaction_tuple.encode()).hexdigest()

transaction_data_with_hash = f"{transaction_data} {transaction_hash}"

transactionRedis.set(transaction_key, transaction_data_with_hash)