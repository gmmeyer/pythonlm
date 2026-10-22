left = 3
while left >= 0:
    if left == 1:
        print("1 task left")
    elif left == 0:
        print("all done!")
    else:
        print(left, "tasks left")
    left -= 1
