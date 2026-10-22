# grade distribution
a = b = c = 0
score = 55
for i in range(12):
    score = (score * 3 + 7) % 50 + 50
    if score >= 90:
        a += 1
    elif score >= 75:
        b += 1
    else:
        c += 1
print("A", "#" * a)
print("B", "#" * b)
print("C", "#" * c)
