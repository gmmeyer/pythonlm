tom = 17
ann = 9
tom, ann = ann, tom
diff = ann - tom
give = diff // 2
ann -= give
tom += give
print(tom)
print(ann)
