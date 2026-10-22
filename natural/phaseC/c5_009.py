w1 = "karolin"
w2 = "kathrin"
diff = 0
for i in range(len(w1)):
    if w1[i] != w2[i]:
        diff += 1
print("hamming distance:", diff)
