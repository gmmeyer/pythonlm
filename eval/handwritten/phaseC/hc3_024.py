s = "banana"
count = 0
pos = ""
for i in range(len(s)):
    if s[i] == "a":
        count += 1
        pos = pos + str(i)
print(count, pos)
other = 0
for i in range(-1, -len(s) - 1, -1):
    if s[i] != "a":
        other += 1
print(other, count + other == len(s))
