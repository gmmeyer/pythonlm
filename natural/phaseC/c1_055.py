# loan payoff schedule
debt = 500
payment = 80
month = 0
print("month | owed")
while debt > 0:
    month += 1
    debt = debt - payment + debt * 5 // 100
    if debt < 0:
        debt = 0
    print(month, debt, sep=" | ")
print("paid off in", month, "months")
