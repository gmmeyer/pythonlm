# gym: longest streak of consecutive visits in 21 days
streak = 0
longest = 0
for day in range(1, 22):
    if day % 7 == 0 or day % 5 == 0:
        streak = 0
    else:
        streak += 1
        if streak > longest:
            longest = streak
print(longest)
