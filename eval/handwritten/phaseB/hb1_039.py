t = 10
held = False
while t > 0:
    if t == 5 and not held:
        print("hold")
        held = True
        continue
    print(t)
    t -= 1
print("liftoff")
