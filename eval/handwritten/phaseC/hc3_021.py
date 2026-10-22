e = ""
print(len(e), len(e + e), len(e * 7))
s = e + "q" + e
print(s, len(s), s[0] == s[-1])
acc = ""
for i in range(4):
    acc = acc + e
print("[" + acc + "]", acc == e, acc != "")
x = "" + str(0) + ""
print(x, len(x), x == "0")
print(e, e, e, sep="|")
