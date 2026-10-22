# bake sale cookies
dough_g = 900
cookie_g = 35
cookies = dough_g // cookie_g
scraps = dough_g % cookie_g
print("cookies")
print(cookies)
print("dough left over")
print(scraps)

per_sheet = 12
sheets = cookies // per_sheet
extra = cookies % per_sheet
print(sheets)
print(extra)

# bags of 3, the rest get eaten by the baker
bags = cookies // 3
eaten = cookies - bags * 3
price = 2
print(bags * price)
print(eaten)
