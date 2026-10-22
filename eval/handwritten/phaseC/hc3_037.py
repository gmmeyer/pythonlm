for x in range(-2, 3):
    label = x > 0 and "pos" or x < 0 and "neg" or "zero"
    print(x, label, len(label))
v = 0
w = v and "never" or "fallback"
print(w)
k = "" and 5 or -5
print(k)
