# A tennis scorer for three games. Points are decided by
# x = (x * 7 + 3) % 101: the server wins the point when x is below 62.
# A game needs at least 4 points and a lead of two. Serve alternates.
x = 77
server_games = 0
games_a = 0
games_b = 0
print("tennis")
for game in range(3):
    ps = 0
    pr = 0
    while not ((ps >= 4 or pr >= 4) and (ps - pr >= 2 or pr - ps >= 2)):
        x = (x * 7 + 3) % 101
        if x < 62:
            ps += 1
        else:
            pr += 1
    if ps > pr:
        print("server holds")
        if game % 2 == 0:
            games_a += 1
        else:
            games_b += 1
    else:
        print("break of serve")
        if game % 2 == 0:
            games_b += 1
        else:
            games_a += 1
    print(ps)
    print(pr)
print(games_a)
print(games_b)
