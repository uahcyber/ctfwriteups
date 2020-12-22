def diff_lists(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

# known new_sigma -> old_sigma mappings
knowns = {
    "3b": "4f", # O
    "18": "20", # ' '
    "0e": "68", # h
    "0b": "6f", # o
    "05": "6c", # l
    "d7": "79", # y
    "02": "6e", # n
    "07": "69", # i
    "0d": "67", # g
    "d3": "74", # t
    "19": "21", # !
    "c3": "54", # T
    "0c": "65", # e
    "d4": "73", # s
    "09": "61", # a
    # everything below was added after near decryption through guessing/reading carol online
    "0f": "6a", # j
    "06": "6b", # k
    "0a": "6d"  # m
}
old_sigma = "0123456789abcdef"
new_sigma = ['','','','','','','','','','','','','','','','']
# read in file
with open("carol.txt",'r') as f:
    data = f.read()
# break data up into pairs
list_data = [data[i:i+2] for i in range(0, len(data), 2)]
# generate new_sigma
for byte in list_data:
    if byte in knowns.keys():
        mapped = knowns[byte]
        new_sigma[old_sigma.index(list(mapped)[0])] = list(byte)[0]
        new_sigma[old_sigma.index(list(mapped)[1])] = list(byte)[1]
print(f"missing mappings for: {diff_lists(new_sigma,list(old_sigma))[-1:]}")
print(f"new_sigma: {new_sigma}")

# decrypt
for byte in list_data:
    if list(byte)[0] in new_sigma:
        newbyte = old_sigma[new_sigma.index(list(byte)[0])]
        if list(byte)[1] in new_sigma:
            newbyte += old_sigma[new_sigma.index(list(byte)[1])]
            print(chr(int(newbyte,16)),end='')
            continue
    print(byte) # if pair wasn't decrypted