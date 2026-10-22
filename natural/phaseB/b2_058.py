# bakery batches: each batch makes 12, orders come in
bread = 0
batches = 0
for order in range(5, 60, 11):
    while bread < order:
        bread += 12
        batches += 1
    bread -= order
print(bread)
print(batches)
