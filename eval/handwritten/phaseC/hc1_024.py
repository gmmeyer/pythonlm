print("PANCAKES (scaled)")
for guests in range(2, 9, 3):
    fl = 50 * guests
    mk = 75 * guests
    eg = (guests + 1) // 2
    print(f"for {guests}: {fl}g flour, {mk}ml milk, {eg} eggs")
print("whisk", "rest", "fry", sep=" > ")
