balance = 200
rate = 5
print("year", "balance", sep=" | ")
for year in range(1, 9):
    balance = balance + balance * rate // 100
    print(year, balance, sep=" | ")
