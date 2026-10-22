# subtractive Euclid: no modulo, just count the subtractions
a = 91
b = 35
subs = 0
while a != b:
    if a > b:
        a -= b
    else:
        b -= a
    subs += 1
print(a)
print(subs)
