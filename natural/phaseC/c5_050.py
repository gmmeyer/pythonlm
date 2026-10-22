s = "abc123xyz45"
digits = 0
letters = 0
for i in range(len(s)):
    c = s[i]
    if "0" <= c <= "9":
        digits += 1
    elif "a" <= c <= "z":
        letters += 1
print("digits:", digits, "letters:", letters)
