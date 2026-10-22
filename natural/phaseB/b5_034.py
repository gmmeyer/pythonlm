# retry loop: the call works on the first attempt where the state is odd
state = 6
attempt = 0
ok = False
while attempt < 5 and not ok:
    attempt += 1
    state = (state * 5 + 3) % 16
    if state % 2 == 1:
        ok = True
print(attempt)
print(ok)
