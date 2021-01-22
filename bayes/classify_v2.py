ham_count = 0
spam_count = 0
size = 160

for i in range(size):
    with open("%d.txt" % i, "r") as f:
        content = f.read()
    print(content)
    category = int(input())  # 1 for "spam", 0 for "ham"
    if category:
        with open(r"spam\%d.txt" % spam_count, "w") as f:
            f.write(content)
        spam_count += 1
    else:
        with open(r"ham\%d.txt" % ham_count, "w") as f:
            f.write(content)
        ham_count += 1
