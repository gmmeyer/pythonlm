x = 17
seen_big = False
for i in range(12):
    x = (x * 7 + 3) % 101
    if x > 80:
        seen_big = True
        print(x)
print(seen_big)
