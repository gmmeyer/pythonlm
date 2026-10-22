goal = 200
saved = 0
week = 0
reached = False
while reached == False:
    week = week + 1
    saved = saved + 15 + week * 2
    if saved >= goal:
        reached = True
print(week)
print(saved)
