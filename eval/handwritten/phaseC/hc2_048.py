n = 7
path = ""
peak = n
while n != 1:
    if n % 2 == 0:
        n //= 2
        path += "d"
    else:
        n = 3 * n + 1
        path += "u"
    if n > peak:
        peak = n
print(path, len(path), peak)
