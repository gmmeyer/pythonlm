# one reward point per 2 spent; tiers at 50 (silver) and 120 (gold)
spent = 0
for purchase in range(1, 11):
    spent += purchase * 15
points = spent // 2
print(points)
if points >= 120:
    print("gold")
elif points >= 50:
    print("silver")
else:
    print("bronze")
