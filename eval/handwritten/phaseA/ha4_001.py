# A savings account followed month by month.
# Interest is paid as a whole number: 2 percent of the balance, rounded down.
# A monthly fee is charged after the interest is added.

balance = 250
monthly_deposit = 40
fee = 3

print("Month 1")
balance += monthly_deposit
interest = balance * 2 // 100
balance += interest - fee
print(interest)
print(balance)

print("Month 2")
balance += monthly_deposit
interest = balance * 2 // 100
balance += interest - fee
print(interest)
print(balance)

print("Month 3")
# a big withdrawal for a new bicycle
balance -= 180
balance += monthly_deposit
interest = balance * 2 // 100
balance += interest - fee
print(interest)
print(balance)

print("Month 4")
balance += monthly_deposit
interest = balance * 2 // 100
balance += interest - fee
print(interest)
print(balance)

print("Month 5")
# the bank raises the fee by one coin
fee += 1
balance += monthly_deposit
interest = balance * 2 // 100
balance += interest - fee
print(interest)
print(balance)

print("Month 6")
balance += monthly_deposit
interest = balance * 2 // 100
balance += interest - fee
print(interest)
print(balance)

print("--- summary ---")
total_deposits = monthly_deposit * 6
print(total_deposits)
# what the bank gave us minus what it took, ignoring the bicycle
print(balance - 250 + 180 - total_deposits)
