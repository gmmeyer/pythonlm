s = "a" * 4 + "b"
print(s, len(s))
i = 0
while s[i] == "a":
    i += 1
print("first b at", i)
t = s + s
print(t)
count = 0
j = 0
while j < len(t):
    if t[j] != "a":
        count += 1
    j += 1
print(count, t[4], t[-1], t[5])
