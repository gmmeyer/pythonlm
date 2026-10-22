word = "wave"
n = len(word)
for k in range(n):
    r = ""
    for i in range(n):
        r += word[(i + k) % n]
    print(r)
