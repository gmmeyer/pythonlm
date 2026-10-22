a = 0
b = 0
c = 5
first = a or b or c
print(first)
none_found = a or b
print(none_found)
last_truthy = c and 9
print(last_truthy)
mixed = a and 1 or 2
print(mixed)
mixed2 = c and 0 or -3
print(mixed2)
print(c > 0 and c)
print(a > 0 and a)
