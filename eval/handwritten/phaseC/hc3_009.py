a = "col1\tcol2"
b = 'say "hi"'
c = "it's"
print(a, len(a))
print(b, len(b), b[4], b[-1])
print(c, len(c), c[2])
print(a[4] == "\t", b[-1] == '"', c[-2] == "'")
print("x", "y", sep="\t")
print(f"{c}\t{b}")
