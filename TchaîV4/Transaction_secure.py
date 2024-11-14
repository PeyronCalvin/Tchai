from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import cryptography

import requests
import json

user_a = 'MonsieurA'
user_b = 'MonsieurB'
amount = '200'

# Generate an RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Convert public key to string
public_key_str = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')


url_register_userb = 'http://127.0.0.1:5000/register-' + user_b
url_register_usera = 'http://127.0.0.1:5000/register-' + user_a
result_register_userb = requests.post(url_register_userb)
result_register_usera = requests.post(url_register_usera,data=public_key_str)

url = 'http://127.0.0.1:5000/users'

response = requests.get(url)

print(result_register_usera.text)
print(result_register_userb.text)

data = json.loads(response.text)

# Search for assigned user IDs
found_key_usera = None
found_key_userb = None
for key, value in data.items():
    if value.get("name") == user_a:
        found_key_usera = key
    elif value.get("name") == user_b:
        found_key_userb = key
    if found_key_usera != None and found_key_userb != None :
        break

found_key_usera = str(found_key_usera)
found_key_userb = str(found_key_userb)

message = found_key_usera + found_key_userb + amount
# Signing a message with the private key
message_binary = message.encode('utf-8')
signature = private_key.sign(
    message_binary,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

signature_str = signature.hex()


url_transaction = 'http://127.0.0.1:5000/transaction-' + found_key_usera + '-' + found_key_userb + '-' + amount + '-' + signature_str
result_transaction = requests.post(url_transaction)

print(result_transaction.text)