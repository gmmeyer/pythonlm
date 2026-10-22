title = "SALE TODAY"
width = 24
side = (width - len(title)) // 2
print("=" * width)
print(" " * side + title)
print("=" * width)
print(f"title is {len(title)} wide, {side} spaces on the left")
