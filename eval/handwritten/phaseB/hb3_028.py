d = 3
hits = 0
while d >= -3:
    if d != 0 and 9 % d == 0:
        hits += 1
    if d == 0 or 12 // d > 0:
        hits += 10
    d -= 1
print(hits)
print(d)
