# A pancake recipe written for 4 people, scaled to other party sizes.
# We first work out how much each person needs (rounded down),
# then multiply by the number of guests. Eggs are rounded up.

flour = 300
milk = 500
sugar = 60
eggs = 3
base_people = 4

flour_each = flour // base_people
milk_each = milk // base_people
sugar_each = sugar // base_people
print("--- per person ---")
print(flour_each)
print(milk_each)
print(sugar_each)

print("Party of 2")
party = 2
print(flour_each * party)
print(milk_each * party)
print(sugar_each * party)
print((eggs * party + base_people - 1) // base_people)

print("Party of 5")
party = 5
print(flour_each * party)
print(milk_each * party)
print(sugar_each * party)
print((eggs * party + base_people - 1) // base_people)

print("Party of 7")
party = 7
print(flour_each * party)
print(milk_each * party)
print(sugar_each * party)
print((eggs * party + base_people - 1) // base_people)

print("Shopping for the party of 7")
# flour comes in 250 g bags, milk in 300 ml cartons
flour_needed = flour_each * party
bags = (flour_needed + 249) // 250
milk_needed = milk_each * party
# (round up by taking one off, dividing, and adding one back)
cartons = (milk_needed - 1) // 300 + 1
print(bags)
print(cartons)
print(bags * 250 - flour_needed)
print(cartons * 300 - milk_needed)
