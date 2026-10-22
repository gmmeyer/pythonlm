# how many times does the digit 7 appear in 1..29?
count = 0
for n in range(1, 30):
    m = n
    while m > 0:
        if m % 10 == 7:
            count += 1
        m //= 10
print(count)
