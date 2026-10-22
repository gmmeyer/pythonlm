# sum readings until the sentinel 0 shows up
x = 4
total = 0
n = 0
while True:
    x = (x * 7 + 3) % 10
    if x == 0:
        break
    total += x
    n += 1
print(n)
print(total)
