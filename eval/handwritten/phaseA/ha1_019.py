starting_balance_in_dollars = 120
rent_payment = 450
grocery_spend = 86
paycheck_amount = 300
overdraft_fee = 25

current_balance = starting_balance_in_dollars - rent_payment
current_balance -= grocery_spend
print("after rent and groceries")
print(current_balance)

current_balance += paycheck_amount
print("after payday")
print(current_balance)

current_balance -= overdraft_fee
print("final")
print(current_balance)
