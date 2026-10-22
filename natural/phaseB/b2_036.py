# alarm clock: count minutes until 7:00 from 5:40
hour = 5
minute = 40
elapsed = 0
while not (hour == 7 and minute == 0):
    minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    elapsed += 1
print(elapsed)
