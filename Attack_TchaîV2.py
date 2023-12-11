import redis

transactionRedis = redis.Redis(
    host='localhost',
    port=6379,
    db=1,
    decode_responses=True
)

# Use scan_iter to find keys matching the pattern
keys_to_update = [key for key in transactionRedis.scan_iter('transaction_*')]
print(keys_to_update)
transactionRedis.delete(keys_to_update[0])