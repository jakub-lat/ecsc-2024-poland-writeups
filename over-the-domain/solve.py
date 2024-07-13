import json
import base64
from collections import defaultdict as dd

with open('packets.json', 'r') as f:
    packets = json.load(f)


def parse_packet(packet):
    frame_no = packet['_source']['layers']['frame']['frame.number']
    dns = packet['_source']['layers']['dns']
    id = dns['dns.id']
    query = list(dns['Queries'].values())[0]
    domain = query['dns.qry.name']

    return frame_no, id, domain

data = bytearray()

for packet in packets:
    frame_no, id, domain = parse_packet(packet)
    
    segments = domain.split('.')

    if len(segments) > 2:
        x = segments[0]
        dec = base64.b64decode(x.encode())

        print(f'{int(frame_no): 5} {id} {x} {dec}')

        data += dec


with open('data.zip', 'wb') as f:
    f.write(data)
