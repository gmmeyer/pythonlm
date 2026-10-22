dna = "ATGCCGTA"
comp = ""
for i in range(len(dna)):
    b = dna[i]
    if b == "A":
        comp += "T"
    elif b == "T":
        comp += "A"
    elif b == "G":
        comp += "C"
    else:
        comp += "G"
print(dna)
print(comp)
