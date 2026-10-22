# running max and min of a wobbling sequence
x = 20
hi = x
lo = x
for step in range(1, 21):
    if step % 3 == 0:
        x -= 7
    else:
        x += 4
    if x > hi:
        hi = x
    if x < lo:
        lo = x
print(hi)
print(lo)
print(hi - lo)
