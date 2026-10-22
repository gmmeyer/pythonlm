title = "menu"
width = 12
left = (width - len(title)) // 2
right = width - len(title) - left
print("+" + "-" * width + "+")
print("|" + " " * left + title + " " * right + "|")
print("+" + "-" * width + "+")
