t = True
f = False
print(t + t, t * 5, f - t, -t, t // 1)
print(str(t + t), str(t), str(t * 1))
total = 0
for i in range(10):
    total += i % 3 == 0
print(total)
print(f"{t + f} {t and 5} {f or -2} {f and 9}")
