msg = "the quick brown fox jumps"
for i in range(len(msg)):
    print(msg[i], end="")
    if i % 8 == 7:
        print()
print()
