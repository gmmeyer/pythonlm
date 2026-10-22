A = "abcdefgh"
n = len(A)
w = "badge"
for rep in range(2):
    out = ""
    i = 0
    while i < len(w):
        j = 0
        while A[j] != w[i]:
            j += 1
        out += A[n - 1 - j]
        i += 1
    print(w, "<->", out)
    w = out
