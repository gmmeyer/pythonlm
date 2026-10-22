# final grade: homework 20%, midterm 30%, final exam 50%
hw1 = 88
hw2 = 92
hw3 = 75
hw4 = 100
hw = (hw1 + hw2 + hw3 + hw4) // 4
print("homework avg")
print(hw)

midterm = 71
final = 84

# weights in tenths so nothing gets too big
grade = (hw * 2 + midterm * 3 + final * 5) // 10
print("course grade")
print(grade)

needed = 90 - grade
print("points short of an A")
print(needed)
