# digital clock readout
hour = 7
minute = 58
for tick in range(6):
    h = str(hour)
    m = str(minute)
    if hour < 10:
        h = "0" + h
    if minute < 10:
        m = "0" + m
    print(h + ":" + m)
    minute += 1
    if minute == 60:
        minute = 0
        hour += 1
