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
    n = int(board_grid/unit_grid)
    s = (board_grid, board_grid)
    a = np.zeros(s, dtype=int)
    for i in range(0,unit_n):
        a_1 = int((positions[i]-1)/n)
        a_2 = int((positions[i]-n*a_1)/n)
        a[unit_grid*a_1:unit_grid*(a_1+1), unit_grid*a_2:unit_grid*(a_2+1)] = 1
    return a