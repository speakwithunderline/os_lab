from sock import *
from database import *


if __name__ == "__main__":
    init()
    add_file("abc_1", 0, "make", "fls")
    data = search_all()
    for row in data:
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])
        print(row[4])
    data = get_all_files("fls")
    for row in data:
        print(row)
