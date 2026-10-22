word = "abcdeb"
rep = ""
for i in range(len(word)):
    for j in range(i):
        if word[j] == word[i] and rep == "":
            rep = word[i]
if rep == "":
    print("no repeats")
else:
    print("first repeated letter:", rep)
