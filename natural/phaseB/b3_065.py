# how many triangle numbers up to 200 are even?
t = 0
n = 0
evens = 0
while True:
    n += 1
    t += n
    if t > 200:
        break
    if t % 2 == 0:
        evens += 1
print(n - 1)
print(evens)
