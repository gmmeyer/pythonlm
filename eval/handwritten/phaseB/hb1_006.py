# saving up for a new bike
saved = 40
goal = 500
month = 0
halfway_said = False
while saved < goal:
    month = month + 1
    saved = saved + 65
    if saved >= goal // 2 and not halfway_said:
        print("halfway there")
        halfway_said = True
print(month)
print(saved)
