def check(s):
    if s.isdigit():
        if 202 <= int(s):
            print(s)
        else:
            print("There are less than 202 apples! You cheated on me!")
    else:
        print("It is not a number!")
