# how many pizzas? 3 slices a guest, 8 slices a pizza
for guests in range(5, 30, 6):
    slices = guests * 3
    pizzas = (slices + 7) // 8
    spare = pizzas * 8 - slices
    print(pizzas)
    if spare >= 4:
        print("leftovers for lunch")
