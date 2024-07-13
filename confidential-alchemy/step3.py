from pwn import *
import hashlib
import subprocess

p = remote('confidential.ecsc24.hack.cert.pl', 5100)

enc = p.recvall().strip().decode()
enc = bytes.fromhex(enc)

secret_hex = 'a42165856bd618589aa0e89d85f8'
secret = bytes.fromhex(secret_hex)

with open('secret2.bin', 'wb+') as f:
    f.write(secret)

secret_string = secret + hashlib.sha512(secret).hexdigest().encode()

enc_unxored = bytes([a^b for a, b in zip(enc, secret_string)]).replace(b'\x00', b'')

with open('enc.bin', 'wb+') as f:
    f.write(enc_unxored)

flag = subprocess.run(f'openssl enc -d -aes-256-cbc -pbkdf2 -iter 1000001 -salt -a -A -kfile secret2.bin -in enc.bin 2>&1', 
                      shell=True, capture_output=True).stdout.decode().strip()

print(flag)