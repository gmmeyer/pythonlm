done = False
count = 0
while done == False:
    count = count + 1
    if count == 5:
        done = True
if done == True:
    print("finished")
else:
    print("not finished")
print(count)
