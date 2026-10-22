# alarm rings at 7:00 and can be snoozed 9 minutes, at most 3 times
minute = 0
snoozes = 0
awake = False
while not awake:
    if snoozes < 3 and minute < 20:
        snoozes += 1
        minute += 9
    else:
        awake = True
print(snoozes)
print(minute)
