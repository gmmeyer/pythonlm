spin = "|/-\\"
for i in range(10):
    print("working", spin[i % 4], end=" ")
    if i % 5 == 4:
        print()
print("finished")
