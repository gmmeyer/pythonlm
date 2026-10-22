sentence = "one two three"
out = ""
word = ""
for i in range(len(sentence)):
    if sentence[i] == " ":
        out = out + word + " "
        word = ""
    else:
        word = sentence[i] + word
out = out + word
print(out)
