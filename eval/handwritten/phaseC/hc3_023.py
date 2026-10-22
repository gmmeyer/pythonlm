n = 4
print(f"{'-' * n}+{'-' * (n + 2)}")
for w in range(1, 4):
    print(f"|{' ' * w}{w}{' ' * (3 - w)}|")
print(f"{'=' * 0}{'end'}")
