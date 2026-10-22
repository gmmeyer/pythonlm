stages = 3
for i in range(1, stages + 1):
    print(f"[{i}/{stages}] stage {i}", end=" ")
    print("." * (8 - i * 2), end=" ")
    print("ok")
print("pipeline finished")
