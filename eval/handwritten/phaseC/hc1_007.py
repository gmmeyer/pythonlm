t = 6
while t > 0:
    if t == 1:
        label = "last call"
    elif t <= 3:
        label = "almost"
    else:
        label = "waiting"
    print("T-" + str(t), label, sep=" : ")
    t -= 1
print("liftoff!")
