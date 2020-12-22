# 1) translate random hex encoded bytes into readable ascii bytes
# 2) throw result into something like quipquip for statistical analysis
# 3) profit(?)

with open("carol.txt",'r') as f:
    data = f.read()

list_data = [data[i:i+2] for i in range(0, len(data), 2)]
unique = set(list_data)
mapped = {}
big_str = ''
for c,byte in enumerate(unique):
    add = 65
    if c > 25:
        add = 97
        c -= 25
    mapped.update({byte:chr(c+add)})
for i in list_data:
    big_str += mapped[i]
print(f"{mapped}\n{big_str}")