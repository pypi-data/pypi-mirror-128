"""
数据生成的主要逻辑
"""

import numpy as np


def generate_matrix(
        board_grid: int, unit_grid: int, unit_n: int, positions: list
) -> np.ndarray:
    """生成指定布局矩阵
        Args:
            board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
            unit_grid (int): 矩形组件分辨率
            unit_n (int): 组件数
            positions (list): 每个元素代表每个组件的位置
        Returns:
            np.ndarray: 布局矩阵
    """
    side_length = board_grid // unit_grid
    matrix1 = np.zeros(shape=(board_grid, board_grid))
    for value in positions:
        if value % side_length != 0:
            pos_x = value // side_length
            pos_y = value % side_length - 1

        else:
            pos_x = value // side_length - 1
            pos_y = side_length - 1
        x1 = unit_grid * pos_x
        x2 = unit_grid * (pos_x + 1)
        y1 = unit_grid * pos_y
        y2 = unit_grid * (pos_y + 1)
        matrix_one = np.ones(shape=(unit_grid, unit_grid))
        matrix1[x1:x2, y1:y2] = matrix_one
    return matrix1



# TODO: 实现布局矩阵的生成
