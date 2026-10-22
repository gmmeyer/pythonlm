# scrolling marquee
text = "HELLO "
n = len(text)
for start in range(n):
    window = ""
    for k in range(4):
        window = window + text[(start + k) % n]
    print("[" + window + "]")
