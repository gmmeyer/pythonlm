# water bill: first 10 units cost 1, next 10 cost 2, the rest cost 4
usage = 27
bill = 0
unit = 1
while unit <= usage:
    if unit <= 10:
        bill += 1
    elif unit <= 20:
        bill += 2
    else:
        bill += 4
    unit += 1
print(bill)
