# An ant colony over six days. A fifth of the ants go foraging and each
# brings back 2 crumbs; every 4 ants eat 1 crumb; the queen lays one egg
# per 10 crumbs in store, and eggs hatch two days later.

ants = 80
food = 30

print("Day 1")
food += ants // 5 * 2
food -= ants // 4
eggs_a = food // 10
print(food)
print(eggs_a)

print("Day 2")
food += ants // 5 * 2
food -= ants // 4
eggs_b = food // 10
print(food)
print(eggs_b)

print("Day 3")
ants += eggs_a
food += ants // 5 * 2
food -= ants // 4
eggs_a = food // 10
print(ants)
print(food)

print("Day 4")
ants += eggs_b
food += ants // 5 * 2
food -= ants // 4
eggs_b = food // 10
print(ants)
print(food)

print("Day 5: rain")
# nobody goes out, but everyone still eats
ants += eggs_a
food -= ants // 4
print(ants)
print(food)

print("Day 6: anteater")
ants -= ants // 3
ants += eggs_b
food -= ants // 4
print(ants)
print(food)

print("--- colony ---")
print(ants - 80)
print(food // ants)
print(food % ants)
