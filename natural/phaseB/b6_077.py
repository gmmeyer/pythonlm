budget = 25
carry = 0
over_day = 0
for day in range(1, 8):
    spent = (day * 9) % 40
    carry += budget - spent
    if carry < 0 and over_day == 0:
        over_day = day
print(carry)
print(over_day)
