# find the first value in the sequence that exceeds 90
x = 1
count = 0
while True:
    x = (x * 7 + 3) % 101
    count += 1
    if x > 90:
        break
    if count == 50:
        break
print(x)
print(count)
