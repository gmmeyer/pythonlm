# centering three words by hand
w1 = "cat"
w2 = "elephant"
w3 = "ox"
width = 10
pad1 = (width - len(w1)) // 2
pad2 = (width - len(w2)) // 2
pad3 = (width - len(w3)) // 2
print("|" + " " * pad1 + w1 + " " * pad1 + "|")
print("|" + " " * pad2 + w2 + " " * pad2 + "|")
print("|" + " " * pad3 + w3 + " " * pad3 + "|")
