temp = 62
for hour in range(6):
    temp += hour * 4 - 3
    msg = "normal"
    if temp > 75:
        msg = "HOT"
    elif temp < 60:
        msg = "cold"
    print(f"{hour}h temp={temp} {msg}")
