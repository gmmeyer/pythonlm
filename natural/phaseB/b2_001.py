balance = 50
step = 0
while True:
    step += 1
    if step % 2 == 1:
        balance += 30
    else:
        balance -= 45
    if balance < 0:
        print("overdrawn")
        break
    if step >= 12:
        print("ok")
        break
print(balance)
print(step)
