for zone in range(1, 5):
    fare = 2 + zone * 3
    print(f"Zone {zone}: fare {fare}")
    if zone == 4:
        print("Last zone, no transfers")
