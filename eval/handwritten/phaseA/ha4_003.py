# A vending machine that takes 5, 10 and 25 cent coins.
# Chips cost 65, a soda costs 85. Change is paid back with
# as many quarters as possible, then dimes, then nickels.

cash_box = 0
chips_left = 6
soda_left = 4
chips_price = 65
soda_price = 85

print("Customer 1: chips")
# pays with three quarters, one at a time
inserted = 0
inserted += 25
inserted += 25
inserted += 25
change = inserted - chips_price
cash_box += chips_price
chips_left -= 1
quarters = change // 25
change %= 25
dimes = change // 10
change %= 10
print(quarters)
print(dimes)
print(change // 5)

print("Customer 2: soda")
# pays with a dollar
change = 100 - soda_price
cash_box += soda_price
soda_left -= 1
quarters = change // 25
change %= 25
dimes = change // 10
change %= 10
print(quarters)
print(dimes)
print(change // 5)

print("Customer 3: two sodas")
# pays with two dollars
change = 200 - soda_price * 2
cash_box += soda_price * 2
soda_left -= 2
quarters = change // 25
change %= 25
dimes = change // 10
change %= 10
print(quarters)
print(dimes)
print(change // 5)

print("--- machine ---")
print(cash_box)
print(chips_left)
print(soda_left)
print(cash_box // 100)
print(cash_box % 100)
