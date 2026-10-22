abc = "abcdefghijklmnopqrstuvwxyz"
msg = "zap"
k = 4
enc = ""
for i in range(len(msg)):
    j = 0
    while abc[j] != msg[i]:
        j += 1
    enc += abc[(j + k) % 26]
print(msg, enc)
