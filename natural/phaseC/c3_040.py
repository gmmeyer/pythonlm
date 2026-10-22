city = "Oslo"
temp = -3
if temp < 0:
    advice = "wear a heavy coat"
elif temp < 15:
    advice = "bring a jacket"
else:
    advice = "enjoy the sun"
print(f"Weather in {city}: {temp} degrees")
print(f"Advice: {advice}")
