# minutes after midnight -> 12 hour clock
for t in range(15, 860, 140):
    h = t // 60
    m = t % 60
    if h == 0:
        print(12)
    elif h > 12:
        print(h - 12)
    else:
        print(h)
    print(m)
    if h < 12:
        print("AM")
    else:
        print("PM")
