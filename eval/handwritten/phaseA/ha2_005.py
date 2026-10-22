h = 3
h = (h - 7) % 12
print(h)
h = (h - 25) % 12
print(h)
m = 15
m = (m - 100) % 60
print(m)
print((h * 60 + m - 600) % 720)
