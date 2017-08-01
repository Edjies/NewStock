# -*-coding:utf-8 -*-

def sumOfSubArray(array):
    if len(array) == 0:
        return 0

    result = []

    for i in range(0, len(array)):
        sum = array[i]
        result.append(sum)
        for j in range(i + 1, len(array)):
            sum += array[j]
            result.append(sum)

    result.sort()
    return result[-1], result[0]




if __name__ == '__main__':
    a = greatestSumOfSubArray([1, 2, 3, 4, -1, 2, -3, 4])
    print(a)