pw = "sunny42day"
score = 0
if len(pw) >= 8:
    score += 1
has_digit = False
for i in range(len(pw)):
    c = pw[i]
    if c == "0" or c == "1" or c == "2" or c == "3" or c == "4":
        has_digit = True
if has_digit:
    score += 1
if pw != "password":
    score += 1
print("strength", score, "of 3")
if score == 3:
    print("strong")
elif score == 2:
    print("ok")
else:
    print("weak")
