print(1, 0, 0, 1, 0, 1, sep="")
s = "100101"
print(s)
built = ""
for d in range(6):
    built += s[d]
print(built == s, built)
print(10, 0, 101, sep="")
print(1, 0, 0, 1, 0, 1)
x = "1" + "0" * 2 + "1" + "0" + "1"
print(x, x == s, len(x))
