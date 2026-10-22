# how many times does the digit 2 show up in the squares of 1..15?
twos = 0
for n in range(1, 16):
    sq = str(n * n)
    for i in range(len(sq)):
        if sq[i] == "2":
            twos += 1
print("digit 2 appears", twos, "times")
