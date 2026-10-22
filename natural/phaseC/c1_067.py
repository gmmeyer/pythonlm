gross = 640
tax_rate = 20
tax = gross * tax_rate // 100
insurance = 45
net = gross - tax - insurance
print("PAY STUB")
print("--------")
print("Gross:", gross)
print("Tax:", tax)
print("Insurance:", insurance)
print("Net pay:", net)
