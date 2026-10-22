alarm = 390          # 6:30, minutes after midnight
snoozes = 0
up = alarm
while snoozes < 3:
    snoozes += 1
    up += 9
hour = up // 60
minute = up % 60
print(hour)
print(minute)
if up > 415:
    print("late for the bus")
else:
    print("made it")
