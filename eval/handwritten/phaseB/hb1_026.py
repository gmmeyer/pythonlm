# a week of sleep
short_nights = 0
best = 0
for night in range(1, 8):
    hours = 5 + (night * 3) % 5
    if hours < 7:
        short_nights += 1
    if hours > best:
        best = hours
print(short_nights)
print(best)
print(short_nights > 3)
