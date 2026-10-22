word = ""
for i in range(5):
    if i == 0:
        ch = "h"
    elif i == 1:
        ch = "e"
    elif i == 2:
        ch = "l"
    elif i == 3:
        ch = "l"
    else:
        ch = "o"
    word = word + ch
    print(word)
print("Built:", word, "with", len(word), "letters")
