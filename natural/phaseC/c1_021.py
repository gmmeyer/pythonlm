# palindrome check by comparing ends
word = "level"
ok = True
i = 0
j = len(word) - 1
while i < j:
    if word[i] != word[j]:
        ok = False
    i += 1
    j -= 1
if ok:
    print(word, "is a palindrome")
else:
    print(word, "is not a palindrome")
