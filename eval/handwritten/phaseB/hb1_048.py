for speed in range(0, 91, 15):
    if speed == 0:
        print("parked")
    elif 0 < speed <= 25:
        print("school zone ok")
    elif 25 < speed <= 55:
        print("city")
    elif 55 < speed < 75:
        print("highway")
    else:
        print("too fast")
    print(20 <= speed < 70)
