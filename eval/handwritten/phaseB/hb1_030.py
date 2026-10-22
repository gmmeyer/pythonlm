pages = 312
per_day = 25
day = 0
read = 0
while read < pages:
    day += 1
    if day % 7 == 6 or day % 7 == 0:
        today = per_day * 2   # weekends: twice as much
    else:
        today = per_day
    read += today
print(day)
print(read > pages)
