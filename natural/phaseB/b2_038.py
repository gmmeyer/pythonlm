# sentinel loop over a pseudo-random stream
x = 9
total = 0
while True:
    x = (x * 7 + 3) % 101
    if x == 0:
        break
    total += x
    if total > 300:
        break
print(total)
print(x)
