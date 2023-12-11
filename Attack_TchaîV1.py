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
    amount = "0"
    user_b_id = parts[4]
    updated_value = user_a_id + " gave " + amount + " to " + user_b_id + " at " + parts[6]
    transactionRedis.set(key, updated_value)
    print(f"Updated {key} to {updated_value}")