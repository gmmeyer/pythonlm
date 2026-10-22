n = 604
s = str(n)
out = ""
for i in range(len(s) - 1, -1, -1):
    out = out + s[i]
print("digits of", n, "backwards:", out)
print("last digit:", s[-1])
