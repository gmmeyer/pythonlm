pw = "hunter22"
n = len(pw)
print("checking password...")
if n < 6:
    verdict = "too short"
elif n < 10:
    verdict = "medium"
else:
    verdict = "strong"
print("length:", n)
print("strength: " + verdict)
masked = "*" * n
print(f"display: {masked}")
if pw[-1] == pw[-2]:
    print("tip: avoid repeating the last character")
