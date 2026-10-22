a = "eggs"
b = "flour"
c = "sugar"
d = "butter"
count = 0
count += 1
print(count, a, sep=". ")
count += 1
print(count, b, sep=". ")
count += 1
print(count, c, sep=". ")
count += 1
print(count, d, sep=". ")
print(f"{count} things to buy")
longest = a
if len(b) > len(longest):
    longest = b
if len(c) > len(longest):
    longest = c
if len(d) > len(longest):
    longest = d
print("longest word:", longest)
