word = "mid"
for w in range(5, 9):
    pad = w - len(word)
    left = pad // 2
    print("[" + "." * left + word + "." * (pad - left) + "]", w)
