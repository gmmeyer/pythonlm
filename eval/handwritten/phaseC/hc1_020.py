total = 0
price = 4
for n in range(1, 6):
    total += price
    print("item " + str(n) + ": " + str(total), end=" | ")
    price += 3
print("END")
print("checkout total =", total)
