# A right-pointing arrow: a shaft of '=' with a head of '>' rows.
shaft = 10
head = 4
for r in range(head):
    print(" " * shaft + ">" * (r + 1))
print("=" * shaft + ">" * (head + 1))
for r in range(head - 1, -1, -1):
    print(" " * shaft + ">" * (r + 1))
print("length", shaft + head + 1, sep=": ")
# and a smaller one pointing left
print("<" + "-" * 6)
print("<<" + "-" * 5, "back", sep="  ")
print("<" + "-" * 6)
