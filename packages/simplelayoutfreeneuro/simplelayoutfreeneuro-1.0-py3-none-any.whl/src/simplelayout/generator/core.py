"""
数据生成的主要逻辑
"""


import numpy as np
import sys


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
    board = np.zeros((board_grid, board_grid))
    assert unit_n == len(positions), \
        sys.exit("the component number (unit) dismatch with position numbder")
    for i in range(unit_n):
        pos = positions[i]
        col = (pos - 1) % unit_grid
        row = (pos - 1) // unit_grid
        board[
            row*unit_grid:(row+1)*unit_grid,
            col*unit_grid:(col+1)*unit_grid
            ] = 1
    return board
