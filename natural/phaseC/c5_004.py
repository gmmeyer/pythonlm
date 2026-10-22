s = "the quick brown fox jumps"
na = ne = ni = no = nu = 0
for i in range(len(s)):
    if s[i] == "a":
        na += 1
    elif s[i] == "e":
        ne += 1
    elif s[i] == "i":
        ni += 1
    elif s[i] == "o":
        no += 1
    elif s[i] == "u":
        nu += 1
print("a:", na, "e:", ne, "i:", ni, "o:", no, "u:", nu)
