# Pizza night for a group of friends, several evenings in a row.
# Slices are shared evenly; slices that do not divide evenly go to the dog.
# A pizza costs 12 coins and the bill is split, rounding each share up.

per_pizza = 8
price = 12
dog = 0

print("Friday")
pizzas = 3
friends = 5
slices = pizzas * per_pizza
dog += slices % friends
print(slices // friends)
bill = pizzas * price
print((bill + friends - 1) // friends)

print("Saturday")
pizzas = 7
friends = 9
slices = pizzas * per_pizza
dog += slices % friends
print(slices // friends)
bill = pizzas * price
print((bill + friends - 1) // friends)

print("Sunday: cut in 12")
per_pizza = 12
pizzas = 2
friends = 7
slices = pizzas * per_pizza
dog += slices % friends
print(slices // friends)
bill = pizzas * price
print((bill + friends - 1) // friends)

print("Monday: one small pizza")
per_pizza = 6
pizzas = 1
friends = 4
slices = pizzas * per_pizza
dog += slices % friends
print(slices // friends)
bill = pizzas * price
print((bill + friends - 1) // friends)

print("--- the dog ---")
print(dog)
# in whole 8-slice pizzas plus extra slices
print(dog // 8)
print(dog % 8)
