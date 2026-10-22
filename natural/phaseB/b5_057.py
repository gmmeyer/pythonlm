# longest stretch without a multiple of 6 or 10 below 50
last = 0
widest = 0
for n in range(1, 50):
    if n % 6 == 0 or n % 10 == 0:
        if n - last > widest:
            widest = n - last
        last = n
print(widest)
