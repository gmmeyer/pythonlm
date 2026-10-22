phrase = "portable network graphics"
acro = phrase[0]
for i in range(1, len(phrase)):
    if phrase[i - 1] == " ":
        acro += phrase[i]
print(acro)
