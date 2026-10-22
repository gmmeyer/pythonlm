code = "x4y7z12"
nums = ""
chars = ""
for i in range(len(code)):
    c = code[i]
    if "0" <= c <= "9":
        nums += c
    else:
        chars += c
print("letters:", chars)
print("digits:", nums)
