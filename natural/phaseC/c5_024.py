bits = "0001110011"
out = ""
groups = 0
run = 1
for i in range(1, len(bits) + 1):
    if i < len(bits) and bits[i] == bits[i - 1]:
        run += 1
    else:
        out += bits[i - 1] + ":" + str(run) + " "
        groups += 1
        run = 1
print(out)
print(groups, "groups")
