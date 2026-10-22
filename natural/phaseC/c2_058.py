text = "one\ntwo\nthree\nfour\n"
lines = 0
for i in range(len(text)):
    if text[i] == "\n":
        lines += 1
print("lines:", lines)
