name = "Dana"
score = 74
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(f"{name} scored {score} and got a {grade}")
needed = 80 - score
if needed > 0:
    print(f"{name} needs {needed} more points for a B")
else:
    print(f"{name} already has a B or better")
