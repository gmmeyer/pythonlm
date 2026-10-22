# single elimination bracket, odd team out gets a bye
teams = 50
rounds = 0
while teams > 1:
    if teams % 2 == 1:
        teams += 1
    teams //= 2
    rounds += 1
    print(teams)
print(rounds)
