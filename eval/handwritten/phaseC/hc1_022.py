slices = 8
pizzas = 3
people = 7
total = slices * pizzas
each = total // people
spare = total % people
print(f"{pizzas} pizzas = {total} slices")
print("each of", people, "gets", each, end="")
if spare > 0:
    print(",", spare, "left over")
for p in range(1, spare + 1):
    print("person " + str(p) + " gets an extra slice")
