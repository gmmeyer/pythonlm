evens = 0
odds = 0
for n in range(1, 21):
    if n % 2 == 0:
        evens += 1
    else:
        odds += 1
print(evens)
print(odds)
