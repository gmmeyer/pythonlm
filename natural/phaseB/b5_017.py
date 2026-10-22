# trailing zeros of 10! come from factors of 5 in 1..10
fives = 0
for k in range(1, 11):
    m = k
    while m % 5 == 0:
        m //= 5
        fives += 1
print(fives)
# and in 1..25
fives = 0
for k in range(1, 26):
    m = k
    while m % 5 == 0:
        m //= 5
        fives += 1
print(fives)
