bs = "\\"
dq = '"'
sq = "'"
print(bs, dq, sq, len(bs), len(dq + sq))
s = dq + "x" + dq
print(s, len(s), s[0] == s[-1], s[1])
p = sq + bs + sq
print(p, len(p), p[1] == bs)
print(f"{dq}{sq}{bs}")
