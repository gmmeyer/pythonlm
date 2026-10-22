# a tiny spinner
frames = "|/-\\"
for i in range(10):
    print("loading " + frames[i % 4])
print("done")
