# pomodoro day: 25 minutes on, 5 off, 15 off after every 4th
work_minutes = 0
break_minutes = 0
for session in range(1, 9):
    work_minutes += 25
    if session == 8:
        break        # done for the day, no break after the last one
    if session % 4 == 0:
        break_minutes += 15
        print("long break")
        continue
    break_minutes += 5
print(work_minutes)
print(break_minutes)
print(work_minutes + break_minutes)
