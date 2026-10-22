# No random module yet, so we roll our own dice with a tiny generator:
#   seed = (seed * 9 + 4) % 107
# and a die shows seed % 6 + 1. Red and Blue each roll once per round.

seed = 42
red = 0
blue = 0

print("Round 1")
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
red += die
print(die)
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
blue += die
print(die)

print("Round 2")
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
red += die
print(die)
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
blue += die
print(die)

print("Round 3")
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
red += die
print(die)
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
blue += die
print(die)

print("Round 4")
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
red += die
print(die)
seed = (seed * 9 + 4) % 107
die = seed % 6 + 1
blue += die
print(die)

print("--- totals ---")
print(red)
print(blue)
print(red - blue)
print(seed)
