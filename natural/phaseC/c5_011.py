word = "rotator"
rev = ""
i = len(word) - 1
while i >= 0:
    rev += word[i]
    i -= 1
print(word, rev)
if word == rev:
    print("palindrome")
else:
    print("not a palindrome")
