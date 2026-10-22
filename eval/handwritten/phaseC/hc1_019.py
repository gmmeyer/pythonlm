s1 = "Ivy"
s2 = "absent"
s3 = "Kofi"
s4 = "absent"
s5 = "Lena"
here = 0
roll = ""
if s1 != "absent":
    here += 1
    roll += s1 + " "
if s2 != "absent":
    here += 1
    roll += s2 + " "
if s3 != "absent":
    here += 1
    roll += s3 + " "
if s4 != "absent":
    here += 1
    roll += s4 + " "
if s5 != "absent":
    here += 1
    roll += s5 + " "
print("present:", roll)
print(f"{here} here, {5 - here} missing")
