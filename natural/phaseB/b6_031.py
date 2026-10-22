# how many hours of daylight when the sun is up between 7 and 19?
daylight = 0
night = 0
for hour in range(24):
    if 7 <= hour < 19:
        daylight += 1
    else:
        night += 1
print(daylight)
print(night)
print(daylight > night)
