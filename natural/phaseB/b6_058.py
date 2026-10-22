# bottle deposit: 5 per bottle plus a bonus of 10 for each full dozen
bottles = 30
refund = 0
for b in range(1, bottles + 1):
    refund += 5
    if b % 12 == 0:
        refund += 10
print(refund)
