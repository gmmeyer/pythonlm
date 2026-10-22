a = "llohe"
b = "hello"
n = len(a)
shift = -1
if n == len(b):
    k = 0
    while k < n and shift < 0:
        i = 0
        while i < n and a[(i + k) % n] == b[i]:
            i += 1
        if i == n:
            shift = k
        k += 1
print(a, b, "shift", shift)
