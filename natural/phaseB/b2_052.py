# score multiplier that grows with each success and resets on failure
score = 0
mult = 1
for turn in range(1, 16):
    if turn % 6 == 0:
        mult = 1
    else:
        score += 5 * mult
        if mult < 4:
            mult += 1
print(score)
print(mult)
