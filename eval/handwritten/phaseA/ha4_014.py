# A child's savings jar, week by week.
# Allowance is 15 coins a week. A fifth of the jar (rounded down)
# goes on sweets, and grandma adds 7 coins on even weeks.

jar = 10
allowance = 15
sweets = 0
received = 0

print("Week 1")
jar += allowance
received += allowance
spent = jar // 5
jar -= spent
sweets += spent
print(jar)

print("Week 2")
jar += allowance + 7
received += allowance + 7
spent = jar // 5
jar -= spent
sweets += spent
print(jar)

print("Week 3")
jar += allowance
received += allowance
spent = jar // 5
jar -= spent
sweets += spent
print(jar)

print("Week 4")
jar += allowance + 7
received += allowance + 7
spent = jar // 5
jar -= spent
sweets += spent
print(jar)

print("Week 5: raise")
allowance += 5
jar += allowance
received += allowance
spent = jar // 5
jar -= spent
sweets += spent
print(jar)

print("Week 6: a toy for 30")
jar += allowance + 7
received += allowance + 7
jar -= 30
spent = jar // 5
jar -= spent
sweets += spent
print(jar)

print("--- summary ---")
print(received)
print(sweets)
print(jar)
print(10 + received - sweets - jar)
