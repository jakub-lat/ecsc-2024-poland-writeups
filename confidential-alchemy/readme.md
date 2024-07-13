# [confidentialAlchemy](https://hack.cert.pl/challenge/confiAlchemy)

## Task

Crypto challenge with AES, xors, and sha512 using openssl and perl.

## Solution

```
enc_aes=`openssl enc -aes-256-cbc -pbkdf2 -iter 1000001 -salt -a -A -kfile "$secrets_file" -in $flag_file`
```

OpenSSL prepends the ciphertext with `Salted__`, and base64-encodes the result. With that, we know the first 10 bytes of the XOR key.


```
sha512 = secreeeeeeeeet + sha512(secret           )
142    = 14             + 128

enc    = Salted__ + ecsc24{ + [..] + [........] + }
142    = 10         7         7    + 127        + 1
```

Also, the flag is much shorter than combined secret+secret_sum -> so, the secret will be xored with null bytes, which allows us to retreive the sha512sum suffix.

### Step 1

Obtain secret prefix and sha512sum suffix

[step1.py](./step1.py)

### Step 2

Brute force the remaining 4 bytes of XOR secret, comparing sha512sums with the known sha512 suffix

[step2/src/main.rs](./step2/src/main.rs)

This took about 1 hour.

### Step 3

Unxor the ciphertext and decode the flag

[step3.py](./step3.py)


`ecsc24{Flag__MoreCryptoMoreSecure!!!!111oneone}`