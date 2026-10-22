# bonus points: double after the tenth point, triple after the twentieth
score = 0
for hit in range(1, 31):
    if hit <= 10:
        score += 1
    elif hit <= 20:
        score += 2
    else:
        score += 3
print(score)
