n = 1
found = False
while not found:
    if n * n > 150:
        found = True
    else:
        n += 1
print(n)
