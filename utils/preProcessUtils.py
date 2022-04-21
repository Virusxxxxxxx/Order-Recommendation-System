from typing import List


def sortCategories(a: List[str]):
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if int(a[j][-1]) > int(a[j + 1][-1]):
                temp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = temp
    return a
