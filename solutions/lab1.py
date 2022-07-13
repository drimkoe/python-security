from hashlib import md5

hex_a = bytearray.fromhex('0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef')

hex_b = bytearray.fromhex('0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef')

digest_a = md5(hex_a).digest()
digest_b = md5(hex_b).digest()

print(hex_a == hex_b)
print(digest_a == digest_b)