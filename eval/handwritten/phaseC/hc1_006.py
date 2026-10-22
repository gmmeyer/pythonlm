first = "Grace"
middle = "Brewster"
last = "Hopper"
ini = first[0] + "." + middle[0] + "." + last[0] + "."
print("initials:", ini)
print(f"badge: {last}, {first[0]}. {middle[0]}.")
print("tag", first[0] + last[0], sep="=")
print("letters in name", len(first) + len(middle) + len(last), sep=" -> ")
