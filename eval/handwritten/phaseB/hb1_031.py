# checking account: paycheck in, one purchase out, every week
balance = 120
for week in range(1, 7):
    balance += 40
    want = 25 + week * 12
    if want > balance:
        print("declined")
        continue
    balance -= want
    print(balance)
