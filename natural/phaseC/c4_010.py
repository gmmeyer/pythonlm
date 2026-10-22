card = "5500123456781234"
hidden = "*" * (len(card) - 4)
tail = card[-4] + card[-3] + card[-2] + card[-1]
print(hidden + tail)
print("ends with", tail)
