secs = 125
while secs >= 115:
    m = secs // 60
    s = secs % 60
    if s < 10:
        print(f"{m}:0{s}")
    else:
        print(f"{m}:{s}")
    secs -= 3
print("time!")
