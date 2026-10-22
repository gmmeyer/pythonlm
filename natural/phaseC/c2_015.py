data = "aaabccdddd"
out = ""
count = 1
for i in range(1, len(data)):
    if data[i] == data[i - 1]:
        count += 1
    else:
        out = out + data[i - 1] + str(count)
        count = 1
out = out + data[-1] + str(count)
print(data, "->", out)
