# 3 km jog in 16:12, what's the pace per km
dist_km = 3
mins = 16
secs = 12
total_s = mins * 60 + secs
pace = total_s // dist_km
print(pace // 60)
print(pace % 60)
