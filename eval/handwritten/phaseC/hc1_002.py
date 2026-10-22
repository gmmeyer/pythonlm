name = "Rosa"
age = 31
sender = "Tom & Ali"
msg = "Happy birthday, " + name + "!"
width = len(msg) + 4
print("*" * width)
print("* " + msg + " *")
print("*" * width)
print(f"{age} looks good on you.")
print("love,", sender, sep="\n  ")
