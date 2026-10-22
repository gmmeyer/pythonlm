# one step reading every 3 hours (in hundreds), 8 readings a day; resets at midnight
steps = 0
goal_days = 0
for reading in range(24):
    if reading % 8 == 0:
        steps = 0
    steps += 5 + reading % 3 + reading // 8 * 3
    if reading % 8 == 7:
        print(steps)
        if steps >= 60:
            goal_days += 1
print(goal_days)
