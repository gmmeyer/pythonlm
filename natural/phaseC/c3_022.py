for i in range(1, 6):
    for j in range(1, 6):
        if i == j:
            mark = "*"
        else:
            mark = ""
        print(str(i * j) + mark, end="\t")
    print()
print("(* marks the squares)")
