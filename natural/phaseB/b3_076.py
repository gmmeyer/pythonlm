# a staircase: each step line is a count, groups divided by a rule
for height in range(1, 4):
    for step in range(height, 0, -1):
        print(step)
    print("=====")
print("end")
