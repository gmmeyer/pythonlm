# odd squares less than 400, with a counter of how many
count = 0
n = 1
while n * n < 400:
    if n % 2 == 1:
        print(n * n)
        count += 1
    n += 1
print(count)
