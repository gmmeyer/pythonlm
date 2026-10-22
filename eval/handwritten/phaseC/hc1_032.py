for trial in range(2):
    if trial == 0:
        word = "level"
    else:
        word = "lever"
    n = len(word)
    i = 0
    same = True
    while i < n // 2:
        if word[i] != word[n - 1 - i]:
            same = False
            break
        i += 1
    if same:
        print(word, "reads the same both ways")
    else:
        print(word, "is not a palindrome (" + word[i] + " vs " + word[n - 1 - i] + ")")
