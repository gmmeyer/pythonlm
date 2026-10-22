level = 100
while level > 0:
    blocks = level // 20
    print("[" + "#" * blocks + "." * (5 - blocks) + "]", str(level) + "%")
    level -= 25
print("battery dead")
