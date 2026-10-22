# A flag: a canton of alternating '*' rows next to '=' stripes,
# followed by full-width stripes below the canton.
w = 24
cw = 9
rows = 9
for r in range(rows):
    if r < 5:
        if r % 2 == 0:
            canton = "* * * * *"
        else:
            canton = " * * * * "
        rest = w - cw
    else:
        canton = ""
        rest = w
    if r % 2 == 0:
        stripe = "=" * rest
    else:
        stripe = "-" * rest
    print("|" + canton + stripe)
print("|")
print("|")
print("pole height", rows + 2, sep=": ")
