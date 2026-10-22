text = "Hello there! How are you? I am fine. Thanks."
enders = 0
for i in range(len(text)):
    c = text[i]
    if c == "." or c == "!" or c == "?":
        enders += 1
print(enders, "sentences")
