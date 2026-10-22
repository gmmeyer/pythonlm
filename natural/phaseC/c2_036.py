n = 676
s = str(n)
rev = ""
for i in range(len(s)):
    rev = s[i] + rev
if s == rev:
    print(n, "is a palindrome")
else:
    print(n, "is not a palindrome")
