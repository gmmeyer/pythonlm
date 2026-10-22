# Four lamps display a 4-bit counter that wraps after 15. Each tick the
# counter goes up by one; we compare old and new lamp by lamp (using // and
# %) to count how many lamps flip, which shows the carry rippling along.
count = 4
flips_total = 0
print("lamp counter")
for tick in range(6):
    old = count
    count = (count + 1) % 16
    flips = 0
    a = old
    b = count
    for lamp in range(4):
        if a % 2 != b % 2:
            flips += 1
        a //= 2
        b //= 2
    flips_total += flips
    print(count)
    print(flips)
print("total flips")
print(flips_total)
