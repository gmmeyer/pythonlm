t = "bananarama"
p = "ana"
pos = ""
i = 0
while i + len(p) <= len(t):
    j = 0
    while j < len(p) and t[i + j] == p[j]:
        j += 1
    if j == len(p):
        pos += str(i) + " "
    i += 1
print("found at:", pos)
