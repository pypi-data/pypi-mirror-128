import numpy as np


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.array:
    # 实现布局矩阵的生成
    # 1. 相当于区域边长划分为length个
    length = int(board_grid / unit_grid)
    # 2. ？？
    length1 = int((board_grid**2) / unit_grid)
    # 3. 构建行列均为board_grid的零矩阵
    img_stride = np.zeros((board_grid, board_grid))

    img_stride = np.lib.stride_tricks.as_strided(
        img_stride,
        shape=(unit_grid, unit_grid, length, length),   # 要输出矩阵的shape
        strides=img_stride.itemsize * \
        np.array([length1, length, board_grid, 1])
    )

    # 求positions对应分块矩阵的坐标
    divis = []       # 横坐标
    remainder = []   # 纵坐标
    for i in positions:     # positions = [2,4,6]，这个顺序就是一排一排走下去的
        divis.append((i-1)//length)    # 减去1是由于python位置从左到右标号为从0开始
        remainder.append((i-1) % length)
    z = list(zip(divis, remainder))

    # 将布局块矩阵填入
    fil = np.ones((unit_grid, unit_grid), int)
    for i in z:
        img_stride[i] = fil

    # 将分块矩阵拼接回去
    a = img_stride[0]
    for i in range(length-1):
        b = img_stride[i+1]
        img1 = np.concatenate((a, b), axis=1)
        a = img1
    a = img1[0]
    for i in range(length-1):
        b = img1[i+1]
        image = np.concatenate((a, b), axis=1)
        a = image
    return image
