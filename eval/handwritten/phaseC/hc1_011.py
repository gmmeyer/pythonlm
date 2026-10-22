name = "Dmitri"
role = "volunteer"
inner = len(role) + 2
pad = inner - len(name)
print("+" + "-" * inner + "+")
print("|" + " " + name + " " * (pad - 1) + "|")
print("|" + " " + role + " " + "|")
print("+" + "-" * inner + "+")
print("HELLO my name is", name, end="!\n")
