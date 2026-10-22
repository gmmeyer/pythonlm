# game score with bonus rules
score = 0
streak = 0
for game in range(1, 13):
    if game % 4 == 0:
        streak = 0
    else:
        streak += 1
        score += 10
        if streak >= 3:
            score += 15
print(score)
print(streak)
if score > 150:
    print("gold")
elif score > 100:
    print("silver")
else:
    print("bronze")
