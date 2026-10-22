# a pill every 4 hours, but not while asleep (23:00 to 7:00)
hour = 7
taken = 0
while hour < 23:
    taken += 1
    hour += 4
print(taken)
print(hour)
