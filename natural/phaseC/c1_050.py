n = 7
for rep in range(3):
    s = str(n)
    print("+" * (len(s) + 4))
    print("+ " + s + " +")
    print("+" * (len(s) + 4))
    n = n * 5
