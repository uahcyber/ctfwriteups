from pwn import *
from math import floor, isqrt
import subprocess

# https://rosettacode.org/wiki/Prime_decomposition#Python:_Using_floating_point 
# ended up not using this
def fac(n):
    step = lambda x: 1 + (x<<2) - ((x>>1)<<1)
    maxq = int(floor(isqrt(n)))
    d = 1
    q = 2 if n == ((n>>1)<<1) else 3
    while q <= maxq and n % q:
        q = step(d)
        d += 1
    return [q] + fac(n // q) if q <= maxq else [n]

def real_fast_factor(n):
    # we out here
    # being lazy
    result = subprocess.run(['./more_primes',str(n)],stdout=subprocess.PIPE)
    return [int(res) for res in result.stdout.decode().strip().split(',')]

def get_decomp(n):
    factors = real_fast_factor(n) # fac(n)
    decomp = []
    for i in set(factors):
        decomp.append({"coef":i,"exp":factors.count(i)})
    return decomp

def reduce_lcm(lcm_decomp,gcd):
    gl_decomp = []
    for factor in lcm_decomp:
        if not gcd % factor["coef"]:
            count = 0
            div = gcd
            while 1:
                count += 1
                div //= factor["coef"]
                if div % factor["coef"]:
                    break
            if count == factor["exp"]:
                continue # don't add this to new_ldecomp
        gl_decomp.append(factor)
    return gl_decomp

# connect to remote challenge
conn = remote('challs.xmas.htsp.ro',6050)
count = 0 # question counter
while True:
    conn.recvuntil('\ngcd(x, y) = ')
    gcd = int(conn.recvuntil('\n').rstrip()) # get gcd
    conn.recvuntil('lcm(x, y) = ')
    lcm = int(conn.recvuntil('\n').rstrip()) # get lcm
    print(lcm)
    count += 1
    if lcm == gcd: # don't waste time decomposing if equal
        conn.sendline(b'1')
        ret = conn.recvline().decode()
        if "That is not the correct answer!" in ret:
            break
        continue
    lcm_decomp = get_decomp(lcm) # get prime power decomp of lcm
    gl_decomp = reduce_lcm(lcm_decomp,gcd) # prune lcm decomp
    conn.sendline(str(1 << len(gl_decomp)).encode()) # send 2^len(gl_decomp)
    try:
        ret = conn.recvline().decode()
        print(ret.strip() + " : " + str(count) + f" : sent - {1 << len(gl_decomp)}")
        if count == 100:
            print(conn.recv().decode().strip())
            break
        if "That is not the correct answer!" in ret:
            print(ret.strip())
            break
    except(EOFError):
        print(f"Times up, got to {count}/100!")
        break
conn.close()