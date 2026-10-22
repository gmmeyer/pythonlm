# pass if the average is at least 50 and no exam is under 30
total = 0
lowest = 100
for exam in range(1, 6):
    score = (exam * 37 + 20) % 61 + 25
    total += score
    if score < lowest:
        lowest = score
average = total // 5
print(average)
print(lowest)
print(average >= 50 and lowest >= 30)
