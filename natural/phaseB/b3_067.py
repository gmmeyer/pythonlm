score = 0
for turn in range(1, 11):
    if turn % 2 == 0:
        score += turn
    elif turn % 3 == 0:
        score -= 1
    else:
        continue
    print(score)
