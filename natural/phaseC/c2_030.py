seq = "ATGCGCGATATC"
gc = 0
for i in range(len(seq)):
    if seq[i] == "G" or seq[i] == "C":
        gc += 1
print(f"GC content: {gc}/{len(seq)} = {gc * 100 // len(seq)}%")
