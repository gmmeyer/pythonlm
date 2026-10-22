# count words even when there are extra spaces
text = "  hello   big  world "
words = 0
inside = False
for i in range(len(text)):
    if text[i] == " ":
        inside = False
    elif not inside:
        inside = True
        words += 1
print(words, "words in", len(text), "characters")
