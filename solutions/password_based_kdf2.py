import hashlib
import secrets
import sys
import timeit

iterations = int(sys.argv[1])

def test():
    message = b'Password'
    salt = secrets.token_bytes(16)
    hash_value = hashlib.pbkdf2_hmac('sha256', message, salt,iterations)
    print(hash_value)

if __name__ == '__main__':
    seconds = timeit.timeit('test()',number=10,globals=globals())
    print('Seconds lapsed: %s' % seconds)