# lockers 1..12: locker n is toggled once per divisor, so odd divisor counts stay open
open_count = 0
for n in range(1, 13):
    divisors = 0
    for d in range(1, n + 1):
        if n % d == 0:
            divisors += 1
    if divisors % 2 == 1:
        open_count += 1
        print(n)
print(open_count)
