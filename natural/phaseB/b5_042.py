# pairs of squares (i*i, j*j) summing to 170, two pointers on 0..13
i = 0
j = 13
pairs = 0
while i < j:
    s = i * i + j * j
    if s == 170:
        pairs += 1
        i += 1
        j -= 1
    elif s < 170:
        i += 1
    else:
        j -= 1
print(pairs)
