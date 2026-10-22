# Paying off a loan. The balance is negative: money still owed.
# Every month a twentieth of the balance is added as interest; with a
# negative balance, // rounds toward more debt (-555 // 20 is -28).

balance = -600
payment = 75
interest_total = 0

print("Month 1")
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 2")
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 3")
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 4: raise, pay 100")
payment += 25
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 5")
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 6")
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 7")
interest = balance // 20
balance += interest + payment
interest_total -= interest
print(balance)

print("Month 8: pay it all")
interest = balance // 20
balance += interest
interest_total -= interest
payment = -balance
balance += payment
print(payment)
print(balance)

print("--- loan closed ---")
print(interest_total)
print(600 + interest_total)
