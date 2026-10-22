line = ""
for k in range(-5, 3):
    line = line + str(k) + "|"
print(line)
print(len(line), line[-1], line[0], line[1])
for k in range(3, -3, -1):
    print(k, -k, k * -k, sep="|")
