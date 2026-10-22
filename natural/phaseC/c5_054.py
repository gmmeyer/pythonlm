pw = "sunshine42"
has_digit = False
has_letter = False
for i in range(len(pw)):
    c = pw[i]
    if "0" <= c <= "9":
        has_digit = True
    if "a" <= c <= "z" or "A" <= c <= "Z":
        has_letter = True
if len(pw) >= 8 and has_digit and has_letter:
    print("strong password")
else:
    print("weak password")
