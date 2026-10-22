z = 0
neg = -42
t = True
f = False
s = str(z) + str(neg) + str(t) + str(f)
print(s)
print(len(str(z)), len(str(neg)), len(str(t)), len(str(f)), len(s))
print(str(neg)[0], str(neg)[-1], str(t)[-1], str(f)[0])
m = -neg
print(str(m) == "42", str(-m) == str(neg), str(z) != "")
print(str(3 > 2) + "/" + str(2 > 3))
