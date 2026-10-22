# score board: three players take turns
a = 0
b = 0
c = 0
for turn in range(18):
    who = turn % 3
    if who == 0:
        a += 4
    elif who == 1:
        b += 3
        if turn > 8:
            b += 2
    else:
        c += 5
print(a)
print(b)
print(c)
print(a > b and a > c)
