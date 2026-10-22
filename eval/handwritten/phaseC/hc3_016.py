s = "foo"
t = "bar"
print(f"{s + t}")
print(f"{s}{t}{s}")
print(f"{len(s + t)} {s * 2} {t[-1]}{t[0]}")
print(f"[{s * 0}] [{t + ''}] [{''}]")
print(f"{s == t} {s + t == 'foobar'} {t != 'bar'}")
