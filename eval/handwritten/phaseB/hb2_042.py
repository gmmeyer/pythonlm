c = 0
for n in range(1, 31):
    if n % 2 != 0 and n % 3 != 0 and n % 5 != 0:
        c += 1
print(c)
N = 600
f = N - N // 2 - N // 3 - N // 5 + N // 6 + N // 10 + N // 15 - N // 30
print(f)
print(f == c * 20)
