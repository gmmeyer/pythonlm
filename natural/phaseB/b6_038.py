people = 7
slices = 0
pizzas = 0
need = people * 2
while slices < need:
    pizzas += 1
    slices += 8
print(pizzas)
print(slices - need)
