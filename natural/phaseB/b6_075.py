# a motion needs more than half of the 9 votes
yes = 0
no = 0
for voter in range(9):
    if (voter * voter + 1) % 3 == 0:
        no += 1
    else:
        yes += 1
print(yes)
print(no)
if yes > 4:
    print("motion carried")
else:
    print("motion lost")
