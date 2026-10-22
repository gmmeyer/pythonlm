# the account locks after 3 failed attempts in a row
fails = 0
locked = False
attempt = 0
while attempt < 12 and not locked:
    attempt += 1
    ok = attempt % 4 == 0 or attempt % 7 == 0
    if ok:
        fails = 0
    else:
        fails += 1
    if fails == 3:
        locked = True
print(attempt)
print(locked)
