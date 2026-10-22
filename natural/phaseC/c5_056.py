# letters must come before digits
code = "ab123"
seen_digit = False
valid = True
for i in range(len(code)):
    c = code[i]
    if "0" <= c <= "9":
        seen_digit = True
    elif "a" <= c <= "z":
        if seen_digit:
            valid = False
    else:
        valid = False
print(code, valid)
