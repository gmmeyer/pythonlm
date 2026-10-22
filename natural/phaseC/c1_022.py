# name tag
name = "Dana"
role = "Guide"
w = 14
print("+" + "-" * w + "+")
print("| " + name + " " * (w - 1 - len(name)) + "|")
print("| " + role + " " * (w - 1 - len(role)) + "|")
print("+" + "-" * w + "+")
