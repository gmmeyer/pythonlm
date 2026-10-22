line = ""
for n in range(5, 50, 9):
    if line != "":
        line += ", "
    line += str(n)
print(line)
print("length:", len(line))
