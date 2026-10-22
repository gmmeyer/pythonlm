# Rabbits in a meadow, followed one generation at a time.
# Every 3 rabbits produce 1 baby (rounded down).
# The foxes catch (rabbits % 7) plus one rabbit per fox,
# and every 15 rabbits still alive attract one more fox.

rabbits = 20
foxes = 2

print("Generation 1")
births = rabbits // 3
deaths = rabbits % 7 + foxes
rabbits += births - deaths
foxes += rabbits // 15
print(rabbits)
print(foxes)

print("Generation 2")
births = rabbits // 3
deaths = rabbits % 7 + foxes
rabbits += births - deaths
foxes += rabbits // 15
print(rabbits)
print(foxes)

print("Generation 3")
births = rabbits // 3
deaths = rabbits % 7 + foxes
rabbits += births - deaths
foxes += rabbits // 15
print(rabbits)
print(foxes)

print("Generation 4: a good spring, twice the babies")
births = rabbits // 3 * 2
deaths = rabbits % 7 + foxes
rabbits += births - deaths
foxes += rabbits // 15
print(rabbits)
print(foxes)

# a hard winter: a quarter of the foxes leave the meadow
print("Generation 5: hard winter")
foxes -= foxes // 4
births = rabbits // 3
deaths = rabbits % 7 + foxes
rabbits += births - deaths
print(rabbits)
print(foxes)

print("--- summary ---")
print(rabbits - 20)
print(foxes - 2)
