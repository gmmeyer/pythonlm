x, y = 503, 278
u = x % 10 - y % 10
t = x // 10 % 10 - y // 10 % 10 + u // 10
h = x // 100 - y // 100 + t // 10
print(h)
print(t % 10)
print(u % 10)
print(h * 100 + t % 10 * 10 + u % 10)
print(x - y)
