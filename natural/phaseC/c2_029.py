dna = "GATTACA"
rc = ""
for i in range(len(dna)):
    b = dna[i]
    if b == "A":
        rc = "T" + rc
    elif b == "T":
        rc = "A" + rc
    elif b == "G":
        rc = "C" + rc
    elif b == "C":
        rc = "G" + rc
print("reverse complement of", dna, "is", rc)
