word = "hello"
n = len(word)
for i in range(n):
    row = ""
    for j in range(n):
        if j == i or j == n - 1 - i:
            row += word[j]
        else:
            row += " "
    print(row)
