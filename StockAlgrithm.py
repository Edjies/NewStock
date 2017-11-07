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


def compress_array(array):
    if len(array) == 0:
        return 0

    result = [array[1]]
    dir = 1 if array[1] > 0 else -1
    for i in range(2, len(array)):
        if dir == 1:
            if array[i] >= 0:
                result[-1] += array[i]
            else:
                result.append(array[i])
                dir = -1
        elif dir == -1:
            if array[i] <= 0:
                result[-1] += array[i]
            else:
                result.append(array[i])
                dir = 1
    return result








if __name__ == '__main__':
    print(compress_array([None, -1, -2, 2, 3, -2, -2]))