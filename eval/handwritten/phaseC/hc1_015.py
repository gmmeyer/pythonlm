days = "MTWTFSS"
total = 0
for d in range(7):
    k = (d * 7 + 3) % 10 + 1
    total += k
    print(days[d], "#" * k, k, sep=" ")
print(f"week total: {total}k steps")
avg = total // 7
print("daily average about", avg, end="k\n")
