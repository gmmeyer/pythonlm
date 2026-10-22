up = 0
for svc in range(1, 6):
    if svc % 3 == 0:
        status = "DOWN"
    else:
        status = "UP"
        up += 1
    print("service", svc, status, sep=" - ")
print(f"{up}/5 services up")
