word = "racecar"
same = True
for i in range(len(word) // 2):
    if word[i] != word[len(word) - 1 - i]:
        same = False
if same:
    print(word, "is a palindrome")
else:
    print(word, "is not a palindrome")
print("last letter:", word[-1])
