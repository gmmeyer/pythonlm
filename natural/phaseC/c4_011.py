user = "night_owl"
ok = True
if len(user) < 4:
    ok = False
    print("too short")
if len(user) > 12:
    ok = False
    print("too long")
if user[0] == "_" or user[0] == "-":
    ok = False
    print("bad first character")
if ok:
    print(user, "is valid")
else:
    print(user, "is rejected")
