title = "my first python script"
slug = ""
for i in range(len(title)):
    if title[i] == " ":
        slug += "_"
    else:
        slug += title[i]
print(slug)
