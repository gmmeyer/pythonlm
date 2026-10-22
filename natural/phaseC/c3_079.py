balance = 100
month = 0
while balance < 160:
    month += 1
    interest = balance // 10
    balance = balance + interest + 5
    print(f"Month {month}: balance {balance}")
print(f"Reached {balance} after {month} months")
