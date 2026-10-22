sentence = "the quick brown fox jumps"
words = 1
for i in range(len(sentence)):
    if sentence[i] == " ":
        words += 1
print("words:", words)
