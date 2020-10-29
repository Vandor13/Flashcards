def check():
    try:
        value = int(input())
        if 25 <= value <= 37:
            print(value)
        else:
            print("Correct the error!")
    except ValueError:
        print("Correct the error!")