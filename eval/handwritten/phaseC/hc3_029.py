s = "abc"
t = "ab" + "c"
u = "abd"
print(f"{s == t} {s != t} {s == u} {s != u}")
print(f"{s[0] == u[0]} {s[-1] == u[-1]} {s[2] != u[2]}")
same = s == t
print(same, not same, same and u, same or u)
