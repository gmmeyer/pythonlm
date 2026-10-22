# coffee loyalty card: every 10th coffee is free
card = 0
free = 0
paid = 0
for visit in range(35):
    card += 1
    if card == 10:
        free += 1
        card = 0
    else:
        paid += 1
print(free)
print(paid)
print(card)
