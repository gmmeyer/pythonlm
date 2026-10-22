pw = "banana42"
masked = "*" * len(pw)
print("You typed:", masked)
print("Length:", len(pw))
if len(pw) >= 8:
    print("Good length")
