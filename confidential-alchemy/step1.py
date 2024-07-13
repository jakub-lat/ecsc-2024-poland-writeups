from pwn import *
import base64
import itertools
import hashlib
from tqdm import tqdm
import concurrent.futures

SECRET_LEN = 14
LOCAL = False

context.log_level = 'error'

def receive():
    if LOCAL:
        res = subprocess.run('./chall.sh', shell=True, capture_output=True).stdout.decode().strip()
        return bytes.fromhex(res)
    
    p = remote('confidential.ecsc24.hack.cert.pl', 5100)
    res = p.recvall()
    return bytes.fromhex(res.strip().decode())

ct = receive()

known_prefix = base64.b64encode(b'Salted__')[:-2]

secret_prefix = bytearray([a^b for a, b in zip(ct, known_prefix)])

print(f'found secret prefix: {secret_prefix.hex()} {secret_prefix} ({len(secret_prefix)})')


samples = [receive() for _ in range(5)]

sha512_suffix = bytearray()
for i in range(len(samples[0])-1, 0, -1):
    if all(samples[0][i] == s[i] for s in samples):
        sha512_suffix.append(samples[0][i])
    else:
        break

sha512_suffix.reverse()

if len(sha512_suffix) % 2 == 1:
    sha512_suffix = sha512_suffix[1:]

print(f'found sha512 suffix {sha512_suffix} ({len(sha512_suffix)})')

remaining_len = SECRET_LEN - len(secret_prefix)

print('remaining', remaining_len)