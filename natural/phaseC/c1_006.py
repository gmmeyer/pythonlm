# box around a word
word = "hello"
edge = "+" + "-" * (len(word) + 2) + "+"
print(edge)
print("| " + word + " |")
print(edge)
