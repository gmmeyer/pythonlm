lives = 3
score = 0
for turn in range(1, 16):
    if turn % 5 == 0:
        lives -= 1
        print("ouch")
        if lives == 0:
            break
    else:
        score += turn
print(score)
print(lives)
