# Opening a combination safe. The dial has 100 marks, 0 to 99.
# Turning right adds, turning left subtracts, and % 100 keeps the
# dial on its marks (Python's % never goes negative here).
# The lock remembers the last digit of the last three stops.

dial = 0
code = 0

print("Right 37")
dial = (dial + 37) % 100
code = code % 100 * 10 + dial % 10
print(dial)

print("Left 52")
dial = (dial - 52) % 100
code = code % 100 * 10 + dial % 10
print(dial)

print("Right 140")
dial = (dial + 140) % 100
code = code % 100 * 10 + dial % 10
print(dial)

print("Left 263")
dial = (dial - 263) % 100
code = code % 100 * 10 + dial % 10
print(dial)

print("Right 99")
dial = (dial + 99) % 100
code = code % 100 * 10 + dial % 10
print(dial)

print("Left 7")
dial = (dial - 7) % 100
code = code % 100 * 10 + dial % 10
print(dial)

print("--- lock ---")
print(code)
print(code // 100)
print(code // 10 % 10)
print(code % 10)
