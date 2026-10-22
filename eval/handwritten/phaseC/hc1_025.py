username = "pix"
password = "pix"
problems = 0
if len(username) < 4:
    print("username too short (need 4+)")
    problems += 1
if password == username:
    print("password cannot match username")
    problems += 1
if len(password) < 8:
    print("password needs", 8 - len(password), "more chars")
    problems += 1
if problems == 0:
    print("account created")
else:
    print(f"{problems} problem(s) found")
