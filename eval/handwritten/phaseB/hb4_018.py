# Rock-paper-scissors between two pseudo-random players.
# Ann draws from a = (a * 7 + 3) % 101 and Bob from b = (b * 5 + 11) % 97.
# Moves are 0 = rock, 1 = paper, 2 = scissors. First to four points wins.
a = 12
b = 30
ann = 0
bob = 0
ties = 0
print("rock paper scissors")
while ann < 4 and bob < 4:
    a = (a * 7 + 3) % 101
    b = (b * 5 + 11) % 97
    ma = a % 3
    mb = b % 3
    if ma == mb:
        ties += 1
        print("tie")
    elif (ma - mb) % 3 == 1:
        ann += 1
        print("ann takes it")
    else:
        bob += 1
        print("bob takes it")
print(ann)
print(bob)
print(ties)
