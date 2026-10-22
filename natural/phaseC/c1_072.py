running = 0
sales = 12
print("day | sales | total")
for day in range(1, 8):
    running += sales
    print(day, sales, running, sep=" | ")
    sales = (sales * 3) % 17 + 5
