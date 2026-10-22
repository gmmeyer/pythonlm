counter = 7
prefix = "A"
for k in range(4):
    num = str(counter)
    while len(num) < 3:
        num = "0" + num
    print("Now serving", prefix + num, end="")
    print(" at desk", k % 2 + 1)
    counter += 5
