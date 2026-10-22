# count the perfect squares between 50 and 200
count = 0
r = 1
while r * r <= 200:
    if r * r >= 50:
        count += 1
    r += 1
print(count)
