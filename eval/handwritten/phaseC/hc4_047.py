# Floyd's triangle: consecutive numbers fill rows of growing length.
# Every number is padded to a width of three characters.
num = 1
for row in range(1, 7):
    line = ""
    for k in range(row):
        s = str(num)
        line = line + " " * (3 - len(s)) + s
        num += 1
    print(line)
print("last number:", num - 1)
