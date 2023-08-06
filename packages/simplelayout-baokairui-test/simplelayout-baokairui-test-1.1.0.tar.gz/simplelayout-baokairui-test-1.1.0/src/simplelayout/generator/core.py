"""
数据生成的主要逻辑
"""


import numpy as np


def generate_matrix(
    board_grid: int, unit_grid: int, unit_n: int, positions: list
):
    """生成指定布局矩阵

    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        np.ndarray: 布局矩阵
    """
    # TODO: 实现布局矩阵的生成
    length = int(board_grid / unit_grid)
    length1 = int((board_grid**2)/unit_grid)
    img_stride = np.zeros((board_grid, board_grid))

    img_stride = np.lib.stride_tricks.as_strided(
        img_stride,
        shape=(unit_grid, unit_grid, length, length),  # 要输出矩阵的 shape
        strides=img_stride.itemsize * \
        np.array([length1, length, board_grid, 1])
    )
    # 求positions对应分块矩阵的坐标
    divis = []
    remainder = []
    for i in positions:
        divis.append((i-1)//length)
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
    # print(img1)
    a = img1[0]
    for i in range(length-1):
        b = img1[i+1]
        image = np.concatenate((a, b), axis=1)
        a = image
    # print(image)
    return image
