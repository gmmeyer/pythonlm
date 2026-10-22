for rank in range(1, 6):
    if rank == 1:
        tag = "gold"
    elif rank == 2:
        tag = "silver"
    elif rank == 3:
        tag = "bronze"
    else:
        tag = "none"
    print(f"#{rank} {tag}")
