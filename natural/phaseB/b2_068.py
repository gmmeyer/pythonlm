# how long until the generator produces a small value?
x = 13
count = 0
while x >= 5:
    x = (x * 7 + 3) % 101
    count += 1
    if count > 100:
        break
print(count)
print(x)
