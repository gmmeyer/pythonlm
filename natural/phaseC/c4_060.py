a = "kernel"
b = "shell"
c = "daemon"
best = a
if len(b) > len(best):
    best = b
if len(c) > len(best):
    best = c
print("longest command:", best, "with", len(best), "letters")
