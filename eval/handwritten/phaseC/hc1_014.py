hour = 8
minute = 40
last = ""
print("BUS 12 departures")
for k in range(5):
    mm = str(minute)
    if minute < 10:
        mm = "0" + mm
    print(f"  {hour}:{mm}")
    last = str(hour) + ":" + mm
    minute += 15
    if minute >= 60:
        minute -= 60
        hour += 1
print("last bus at", last)
