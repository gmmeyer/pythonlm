temp = 61
target = 68
steps = 0
while temp != target:
    if temp < target:
        temp += 2   # heater kicks on
    else:
        temp -= 1   # overshot, let it cool off
    steps += 1
    print(temp)
print("holding at target")
print(steps)
