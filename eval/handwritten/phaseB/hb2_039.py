r = 311 % 99
s = 22 % 7
k = 0
for i in range(8):
    r *= 10
    s *= 10
    x = r // 99
    y = s // 7
    r %= 99
    s %= 7
    if x != y:
        print(x)
        print(y)
        break
    k += 1
print(k)
