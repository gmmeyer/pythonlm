total = 0
for i in range(3):
    k = 10
    while k > 0:
        k -= 3
        if k < i * 3:
            break
        total += k
    print(k)
print(total)
