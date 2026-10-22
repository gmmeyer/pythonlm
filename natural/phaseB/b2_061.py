# countdown with three phases
t = 12
while t > 0:
    if t > 8:
        print("prep")
    elif t > 3:
        print("run")
    else:
        print("end")
    t -= 2
