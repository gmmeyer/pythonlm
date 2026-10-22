# parking garage over a ten hour day
capacity = 12
parked = 0
turned_away = 0
for hour in range(1, 11):
    if hour <= 4:
        arriving = 4
    elif hour <= 7:
        arriving = -3
    else:
        arriving = 2
    parked += arriving
    if parked > capacity:
        turned_away += parked - capacity
        parked = capacity
        print("FULL")
print(parked)
print(turned_away)
