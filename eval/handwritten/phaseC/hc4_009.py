# Tic-tac-toe from nine one-character cells after a fixed game.
# X takes the anti-diagonal on the seventh move.
a = b = c = d = e = f = g = h = i = "."
e = "X"
a = "O"
c = "X"
b = "O"
d = "X"
f = "O"
g = "X"
print(a, b, c, sep="|")
print("-+-+-")
print(d, e, f, sep="|")
print("-+-+-")
print(g, h, i, sep="|")
winner = "nobody"
if a != "." and a == b and b == c:
    winner = a
if d != "." and d == e and e == f:
    winner = d
if g != "." and g == h and h == i:
    winner = g
if a != "." and a == e and e == i:
    winner = a
if c != "." and c == e and e == g:
    winner = c
print("winner:", winner)
