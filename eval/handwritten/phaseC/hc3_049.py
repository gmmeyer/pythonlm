s = "zz"
print(f"[{''}][{s * 0}][{'' * 3}][{s[0] * 0}]")
print(f"[{s}{''}{s}]", f"{''}", "end", sep="|")
e = f""
print(len(e), e == "", "[" + e + "]")
n = 0
t = f"{n}" + f"{''}"
print(t, len(t), t == "0")
