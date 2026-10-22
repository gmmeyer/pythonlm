# how many years until 100 grows past 200 at 7% a year
balance = 100
years = 0
while balance <= 200:
    balance += balance * 7 // 100
    years += 1
print(years)
print(balance)
