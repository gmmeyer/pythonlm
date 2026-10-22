s = "abcdefg"
n = len(s)
for i in range(n):
    a = s[i - n]
    b = s[-(i + 1)]
    print(i, i - n, a, b, a == s[i])
