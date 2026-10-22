# count down by two from 9, skipping multiples of 3
for n in range(9, 0, -2):
    if n % 3 == 0:
        continue
    print(n)
