word = "ZIGZAG"
indent = 0
step = 1
for i in range(len(word)):
    print(" " * indent + word[i])
    indent += step
    if indent == 3 or indent == 0:
        step = -step
