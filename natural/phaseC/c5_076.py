# every row starts one letter later
word = "cycle"
n = len(word)
for i in range(n):
    for j in range(n):
        print(word[(i + j) % n], end="")
    print()
