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
    unit_n += 0
    amount_in_length = int(board_grid/unit_grid)
    unit_layout = np.zeros(shape=(board_grid, board_grid))
    for position in positions:
        index_hang = position//amount_in_length
        index_lie = position % amount_in_length
        if index_lie:
            index_lie -= 1

        else:
            index_hang -= 1
            index_lie = amount_in_length-1

        for i in range(unit_grid):
            for j in range(unit_grid):
                unit_layout[index_hang*unit_grid+i, index_lie*unit_grid+j] = 1

    return unit_layout
