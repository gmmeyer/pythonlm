# A trip to the arcade. One coin buys 4 tokens. Games cost tokens
# and pay out tickets; tickets buy prizes at the counter.

coins = 25
tokens = coins * 4
tickets = 0

print("Skee-ball: 4 games at 3")
games = 4
tokens -= games * 3
tickets += 12
tickets += 7
tickets += 30
tickets += 9
print(tokens)
print(tickets)

print("Whack-a-mole: 3 games at 5")
# 2 tickets for every mole hit
games = 3
tokens -= games * 5
moles = 14
tickets += moles * 2
moles = 9
tickets += moles * 2
moles = 21
tickets += moles * 2
print(tokens)
print(tickets)

print("Jackpot wheel: 10 tokens")
tokens -= 10
tickets += 103
print(tokens)
print(tickets)

print("Prize counter")
# a bear costs 150 tickets, erasers cost 8
bears = tickets // 150
tickets %= 150
erasers = tickets // 8
tickets %= 8
print(bears)
print(erasers)
print(tickets)

print("--- going home ---")
# spare tokens are traded back, 4 for a coin
print(tokens // 4)
print(tokens % 4)
