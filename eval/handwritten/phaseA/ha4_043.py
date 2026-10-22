# A teacher shares bags of candy with a class of 23.
# Each time the candy is split evenly between the children present;
# the remainder goes into the teacher's jar.

class_size = 23
jar = 0
every_day = 0

print("Monday: bag of 157")
bag = 157
kids = class_size
every_day += bag // kids
jar += bag % kids
print(bag // kids)
print(jar)

print("Tuesday: 3 absent")
# the jar is emptied into the new bag
bag = 96 + jar
jar = 0
kids = class_size - 3
every_day += bag // kids
jar += bag % kids
print(bag // kids)
print(jar)

print("Wednesday: bag of 64")
bag = 64
kids = class_size
every_day += bag // kids
jar += bag % kids
print(bag // kids)
print(jar)

print("Thursday: 4 helpers")
# the jar is split between the 4 helpers who cleaned up
helpers = 4
print(jar // helpers)
jar %= helpers
print(jar)

print("--- week ---")
# candy for a child who came every day
print(every_day)
print(jar)
