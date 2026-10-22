word = "hello"
width = 11
pad = (width - len(word)) // 2
print("[" + " " * pad + word + " " * (width - len(word) - pad) + "]")
