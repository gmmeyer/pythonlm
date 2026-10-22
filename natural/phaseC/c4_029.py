hour = 7
minute = 5
for step in range(5):
    hh = str(hour)
    mm = str(minute)
    if hour < 10:
        hh = "0" + hh
    if minute < 10:
        mm = "0" + mm
    print(hh + ":" + mm)
    minute += 20
    if minute >= 60:
        minute -= 60
        hour += 1
