letters = "ABCDEFG"
for i in range(len(letters)):
    row = ""
    for j in range(i + 1):
        row = row + letters[j]
    print(row)
