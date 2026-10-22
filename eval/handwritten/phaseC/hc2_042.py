A = "abcdefgh"
text = "headbag"
key = "bed"
out = ""
for i in range(len(text)):
    t = 0
    while A[t] != text[i]:
        t += 1
    k = 0
    while A[k] != key[i % len(key)]:
        k += 1
    out += A[(t + k) % len(A)]
print(text, key, out)
