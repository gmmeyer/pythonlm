passed = 0
failed = 0
score = 40
for i in range(8):
    score = score + 9
    if score >= 60:
        result = "pass"
        passed += 1
    else:
        result = "fail"
        failed += 1
    print("Test", i + 1, "score", score, result)
print("Passed:", passed, "Failed:", failed)
