# Number pyramid: row k counts up 1..k then back down to 1.
n = 6
for k in range(1, n + 1):
    row = ""
    j = 1
    while j <= k:
        row = row + str(j)
        j += 1
    j = k - 1
    while j >= 1:
        row = row + str(j)
        j -= 1
    print(" " * (n - k) + row)
print("last row has", 2 * n - 1, "digits")
