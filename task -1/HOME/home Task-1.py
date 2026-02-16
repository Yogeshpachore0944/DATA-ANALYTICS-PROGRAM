# Top roof
for i in range(1, 10, 2):
    spaces = (9 - i) // 2
    print(" " * spaces + "*" * i + " " + "*" * 16)

# One straight line
print("*" * 10 + " " + "*" * 16)

# Window line (only one window added)
print("**" + " ***  " + "**" + " " + "*" * 16)

# Door (2 lines – same as before)
# for i in range(2):
print("**" + "|----|" + "**" + " " + "*" * 16)
print("**" + "|    |" + "**" + " " + "*" * 16)
print("**" + "|   o|" + "**" + " " + "*" * 16)
print("**" + "|____|" + "**" + " " + "*" * 16)
# Bottom line
print("*" * 10 + " " + "*" * 16)
