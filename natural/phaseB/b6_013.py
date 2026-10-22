# two players roll a deterministic "die"; best of 12 rounds
a = 4
b = 2
score_a = 0
score_b = 0
for round_no in range(12):
    a = (a * 5 + round_no) % 6 + 1
    b = (b * 7 + 2 * round_no + 1) % 6 + 1
    if a > b:
        score_a += 1
    elif b > a:
        score_b += 1
print(score_a)
print(score_b)
print(score_a > score_b)
