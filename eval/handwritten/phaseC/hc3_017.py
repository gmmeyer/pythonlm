a = "ab" + "c"
b = "a" + "bc"
c = "abc" + ""
d = "" + "a" + "" + "bc" + ""
print(a, b, c, d)
print(a == b, b == c, c == d, a != d)
e = "abc" * 1
f = "abc" * 2
print(e == a, f == a + a, f != a * 2, len(f))
g = "ab" + "c "
print(g == a, len(g), "[" + g + "]")
