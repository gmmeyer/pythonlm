bill = 48
for pct in range(10, 25, 5):
    tip = bill * pct // 100
    print(f"{pct}% tip: {tip}, total {bill + tip}")
people = 3
share = (bill + 9) // people
leftover = (bill + 9) % people
print("each pays", share, end="")
if leftover != 0:
    print(" (plus " + str(leftover) + " extra)")
else:
    print(" exactly")
