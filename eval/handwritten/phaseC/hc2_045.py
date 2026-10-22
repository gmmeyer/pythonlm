count = 0
for n in range(118, 135):
    t = str(n)
    i = 0
    j = len(t) - 1
    while i < j and t[i] == t[j]:
        i += 1
        j -= 1
    if i >= j:
        count += 1
        print(t, end=" ")
print("count", count)
