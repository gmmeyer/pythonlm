start_h = 9
start_m = 45
length = 135
total_min = start_m + length
end_h = start_h + total_min // 60
end_m = total_min % 60
print("meeting ends at")
print(end_h)
print(end_m)
