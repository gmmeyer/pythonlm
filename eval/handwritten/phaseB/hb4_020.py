# A bacteria culture doubles every hour up to the dish capacity of 900.
# Whenever the count tops 500 an antibiotic dose is given. The first dose
# leaves a third alive; every later dose is weaker and leaves more alive.
count = 5
doses = 0
print("culture log")
for hour in range(1, 17):
    if count > 450:
        count = 900
    else:
        count = count * 2
    if count > 500:
        doses += 1
        count = count // (doses + 2) * doses
        print("dose given")
    print(count)
print("doses")
print(doses)
print(count < 500)
