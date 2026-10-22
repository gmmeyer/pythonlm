# Ping-pong between A and B. Every hit draws x = (x * 7 + 3) % 101.
# The longer a rally runs, the likelier a miss: the hitter misses when
# x % 10 + rally is above 10. The other player scores. First to 3 wins.
x = 31
score_a = 0
score_b = 0
rally = 0
hitter = 0
print("ping pong")
while score_a < 3 and score_b < 3:
    x = (x * 7 + 3) % 101
    rally += 1
    if x % 10 + rally > 10:
        if hitter == 0:
            score_b += 1
            print("A misses")
        else:
            score_a += 1
            print("B misses")
        print(rally)
        rally = 0
    else:
        hitter = 1 - hitter
print("final score")
print(score_a)
print(score_b)
