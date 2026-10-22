s = "ab"
for n in range(-2, 4):
    t = s * n
    print(n, len(t), "<" + t + ">")
e = "" * 5
print("[" + e + "]", len(e))
k = 3
print("<" + "-" * (k - 3) + ">", "<" + "=" * -k + ">", "<" + "~" * (k * 2) + ">")
