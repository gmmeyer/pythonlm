s = "Room 101, Floor 3!"
d = up = low = other = 0
for i in range(len(s)):
    c = s[i]
    if "0" <= c <= "9":
        d += 1
    elif "a" <= c <= "z":
        low += 1
    elif "A" <= c <= "Z":
        up += 1
    else:
        other += 1
print(f"digits={d} upper={up} lower={low} other={other}")
