s = "attackatdawn"
enc = ""
for i in range(0, len(s), 2):
    enc += s[i]
for i in range(1, len(s), 2):
    enc += s[i]
h = (len(s) + 1) // 2
dec = ""
for i in range(len(s)):
    if i % 2 == 0:
        dec += enc[i // 2]
    else:
        dec += enc[h + i // 2]
print(enc, dec, dec == s)
