s = "aBcDeF"
alt = True
for i in range(len(s) - 1):
    first_low = "a" <= s[i] <= "z"
    next_low = "a" <= s[i + 1] <= "z"
    if first_low == next_low:
        alt = False
print(s, "alternates case:", alt)
