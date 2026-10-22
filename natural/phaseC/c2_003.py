w1 = "planet"
w2 = "plants"
same = 0
i = 0
while i < len(w1) and i < len(w2) and w1[i] == w2[i]:
    same += 1
    i += 1
print("common prefix length:", same)
if same == len(w1) and same == len(w2):
    print("identical")
else:
    print("first difference at index", same)
