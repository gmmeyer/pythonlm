pw = "password"
if pw == "password":
    print("Too common")
elif len(pw) < 8:
    print("Too short")
else:
    print("Accepted")
print("Length was", len(pw))
