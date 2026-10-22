# is the conference room free? times are minutes after 8:00
a_start = 60
a_end = 150
for b_start in range(0, 200, 45):
    b_end = b_start + 30
    if b_end <= a_start or b_start >= a_end:
        print("free")
    else:
        print("conflict")
    print(a_start <= b_start < a_end)
