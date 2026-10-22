# fines at the library: grace period then daily fine, with a cap
fine = 0
for day in range(1, 21):
    if day > 5:
        fine += 2
        if fine >= 24:
            fine = 24
print(fine)
if fine == 24 and not fine < 24:
    print("capped")
