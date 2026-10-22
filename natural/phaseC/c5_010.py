secret = "pass7"
found = -1
for n in range(10):
    guess = "pass" + str(n)
    if guess == secret:
        found = n
        break
print("matched with digit", found)
