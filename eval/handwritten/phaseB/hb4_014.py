# A chess clock. Each player starts with 60 seconds and gains 2 seconds
# after each move. Thinking times come from x = (x * 7 + 3) % 101.
# White also burns 4 extra seconds on every fifth round.
white = 60
black = 60
x = 42
rnd = 0
print("clocks start")
while rnd < 18:
    rnd += 1
    x = (x * 7 + 3) % 101
    white -= x % 10 + 1
    if rnd % 5 == 0:
        white -= 4
    if white <= 0:
        print("white flags")
        break
    white += 2
    x = (x * 7 + 3) % 101
    black -= x % 9 + 2
    if black <= 0:
        print("black flags")
        break
    black += 2
    print(white - black)
print("rounds")
print(rnd)
print(white > black)
