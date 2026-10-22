queue = 0
for minute in range(1, 8):
    if minute % 2 == 1:
        queue += 1
    if minute % 3 == 0 and queue > 0:
        queue -= 1
    if queue == 1:
        print(minute, "- 1 person waiting")
    elif queue == 0:
        print(minute, "- nobody waiting")
    else:
        print(minute, "-", queue, "people waiting")
