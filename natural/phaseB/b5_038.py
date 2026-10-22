# add up multiples of 7 but stop at the first sum over 100
total = 0
k = 0
while True:
    k += 1
    total += 7 * k
    if total > 100:
        break
print(k)
print(total)
