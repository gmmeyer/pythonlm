# values are 3*k for k in 0..40; find two whose sum is 99 and which are 33 apart
i = 0
j = 40
while i < j:
    s = 3 * i + 3 * j
    d = 3 * j - 3 * i
    if s == 99 and d == 33:
        break
    if s > 99:
        j -= 1
    else:
        i += 1
print(3 * i)
print(3 * j)
