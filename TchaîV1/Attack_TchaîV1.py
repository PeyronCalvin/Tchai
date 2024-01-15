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
for key in keys_to_update:
    current_value = transactionRedis.get(key)
    parts = current_value.split(' ')
    user_a_id = parts[0]
    user_b_id = parts[1]
    amount = "0"
    timestamp = parts[3]
    updated_value = user_a_id + " " + user_b_id + " " + amount + " " + timestamp
    transactionRedis.set(key, updated_value)
    print(f"Updated {key} to {updated_value}")
