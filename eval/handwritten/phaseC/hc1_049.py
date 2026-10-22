total = 0
print("LUNCH ORDER")
for k in range(3):
    if k == 0:
        item = "club"
        n = 3
    elif k == 1:
        item = "wrap"
        n = 1
    else:
        item = "melt"
        n = 0
    if n == 0:
        continue
    if n == 1:
        word = item
    else:
        word = item + "s"
    print(f"  {n} x {word}")
    total += n
print("sandwiches:", total, end=" ")
print("(" + str(total * 6) + " dollars)")
