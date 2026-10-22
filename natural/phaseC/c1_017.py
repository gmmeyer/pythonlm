# report card
math = 92
art = 78
history = 85
avg = (math + art + history) // 3
if avg >= 90:
    grade = "A"
elif avg >= 80:
    grade = "B"
elif avg >= 70:
    grade = "C"
else:
    grade = "D"
print("Report Card")
print("===========")
print(f"math: {math}")
print(f"art: {art}")
print(f"history: {history}")
print(f"average {avg} -> grade {grade}")
