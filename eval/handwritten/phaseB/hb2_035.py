t = 50
w = 0
for q in range(0, t // 25 + 1):
    r = t - 25 * q
    for d in range(0, r // 10 + 1):
        w += (r - 10 * d) // 5 + 1
print(w)
