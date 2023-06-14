import string
import random

def generate_secret_key(length=32):
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for _ in range(length))
    return secret_key

secret_key = generate_secret_key()
print('Secret key: ', secret_key)