attempt = 1
ok = False
while not ok and attempt <= 5:
    if attempt == 3:
        ok = True
        print(f"attempt {attempt}: success")
    else:
        print(f"attempt {attempt}: failed, retrying")
    attempt += 1
