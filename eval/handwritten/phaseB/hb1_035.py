limit = 680          # elevator capacity, pounds
load = 0
riders = 0
weight = 150
while True:
    if load + weight > limit:
        print("next car please")
        break
    load += weight
    riders += 1
    weight -= 13
print(riders)
print(load)
