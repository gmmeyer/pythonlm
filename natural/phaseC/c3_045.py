user = "admin"
pw = "1234"
if user == "admin" and pw == "secret":
    print("Welcome back,", user)
elif user == "admin":
    print("Wrong password for", user)
else:
    print("Unknown user")
