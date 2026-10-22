found = 0
for a in range(1, 6):
    for b in range(1, 6):
        if b < a:
            continue
        if a * b == 12:
            found = a * 10 + b
            break
    if found:
        break
print(found)
print(a)
print(b)
