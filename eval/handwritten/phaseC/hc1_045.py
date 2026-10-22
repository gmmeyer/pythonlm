hour = 9
minute = 30
for slot in range(4):
    if slot == 0:
        topic = "welcome"
        length = 10
    elif slot == 1:
        topic = "budget review"
        length = 25
    elif slot == 2:
        topic = "coffee break"
        length = 15
    else:
        topic = "open questions"
        length = 20
    mm = str(minute)
    if minute < 10:
        mm = "0" + mm
    print(str(hour) + ":" + mm, topic, sep="  ")
    minute += length
    while minute >= 60:
        minute -= 60
        hour += 1
print(f"wrap up by {hour}:{minute}")
