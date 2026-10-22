# darts, counting down from 301
remaining = 301
darts = 0
while remaining > 0:
    darts += 1
    if darts % 4 == 0:
        hit = 19
    elif darts % 2 == 0:
        hit = 57
    else:
        hit = 40
    if hit > remaining:
        print("bust")
        break
    remaining -= hit
print(remaining)
print(darts)
