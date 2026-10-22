empty = ""
name = empty or "default"
other = "given" or "default"
both = "left" and "right"
none = empty and "never"
print("[" + name + "]", "[" + other + "]")
print("[" + both + "]", "[" + none + "]", len(none))
zero = 0
pick = zero or "zero was falsy"
print(pick, len(pick))
pick2 = "" or "" or "third"
print(pick2, "" or 0, 0 or "")
print("[", "" or "", "]", sep="")
