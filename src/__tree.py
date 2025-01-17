with open("log.txt", "w", encoding="utf-8") as f:
    for i in range(2020, 2029+1):
        for j in range(1, 12+1):
            print(f"{i}年{j}月\\n", end = "", file=f)