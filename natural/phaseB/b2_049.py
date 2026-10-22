# robot grid walk: x and y
x = 0
y = 0
for step in range(1, 13):
    if step % 4 == 1:
        x += 2
    elif step % 4 == 2:
        y += 3
    elif step % 4 == 3:
        x -= 1
    else:
        y -= 1
print(x)
print(y)
print(x == y)
