text = "abracadabra"
print("positions of a:", end=" ")
for i in range(len(text)):
    if text[i] == "a":
        print(i, end=" ")
print()
