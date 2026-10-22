size = 1
while size < 100:
    unit = "bytes"
    if size == 1:
        unit = "byte"
    print(f"file of {size} {unit}")
    size = size * 3 + 1
