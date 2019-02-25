# -*- coding:utf-8-*-
import numpy as np

def t_create_numpy():
    data = np.array([[1,2,3],[4,5,6]], dtype='int')
    #data = np.empty([1,7], dtype='str')
    print(data)


if __name__ == '__main__':
    t_create_numpy()