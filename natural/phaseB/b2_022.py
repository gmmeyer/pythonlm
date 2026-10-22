# bug colony doubles each day until the dish is full
bugs = 3
day = 0
while True:
    day += 1
    bugs *= 2
    if bugs >= 500:
        bugs = 500
        break
print(day)
print(bugs)
