# numbers from 11 to 29 whose digits are all odd
for n in range(11, 30):
    m = n
    all_odd = True
    while m > 0:
        if m % 10 % 2 == 0:
            all_odd = False
        m //= 10
    if all_odd:
        print(n)
