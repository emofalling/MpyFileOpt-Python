for a in range(1, 10):
    for b in range(0, 10):
        for c in range(0, 10):
            for d in range(0, 10):
                if a**4 + b**4 + c**4 + d**4 == 1000*a + 100*b + 10*c + d:
                    print(1000*a + 100*b + 10*c + d)