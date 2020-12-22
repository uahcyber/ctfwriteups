from pwn import *

# connect to remote challenge instance
conn = remote('challs.xmas.htsp.ro',6051)
cont = True
count = 1
while cont:
    # get data
    dat = conn.recvuntil('array =')
    print(f"question {count}/50")
    if b"50/50" in dat:
        cont = False # this is the last question
    # parse data
    arr = conn.recvuntil('=').decode().split('\n')[0].strip().replace('[','').replace(']','')
    k1 = conn.recvuntil('=').decode().split('\n')[0]
    k2 = conn.recvuntil('\n').decode().strip()
    nums = [int(n) for n in arr.split(',')]
    # sort array in ascending order
    nums.sort()
    # get first k1 elements of sorted array
    first_question = nums[:int(k1)]
    # sort array in descending order
    nums.sort(reverse=True)
    # get first k2 elements of sorted array
    second_question = nums[:int(k2)]
    # format result
    result = ', '.join(str(n) for n in first_question) + '; ' + ', '.join(str(n) for n in second_question)
    conn.sendline(result.encode()) # send
    count += 1
final = conn.recv().decode() # get flag after all questions are answered
print(final)
conn.close()