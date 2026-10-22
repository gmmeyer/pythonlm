# Reverse three words by indexing from the end, and test for palindromes.
for k in range(3):
    if k == 0:
        w = "rotor"
    elif k == 1:
        w = "python"
    else:
        w = "stats"
    rev = ""
    j = len(w) - 1
    while j >= 0:
        rev = rev + w[j]
        j -= 1
    if rev == w:
        verdict = "palindrome"
    else:
        verdict = "not a palindrome"
    print(w + " / " + rev + " : " + verdict)
