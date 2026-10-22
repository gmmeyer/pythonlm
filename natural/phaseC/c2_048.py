a = "karolin"
b = "kathrin"
diff = 0
for i in range(len(a)):
    if a[i] != b[i]:
        diff += 1
print("hamming distance:", diff)
