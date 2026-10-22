for i in range(1, 21):
    word = ""
    if i % 3 == 0:
        word = word + "Fizz"
    if i % 5 == 0:
        word = word + "Buzz"
    if word == "":
        word = str(i)
    print(word)
