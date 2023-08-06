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
    # 用布局板分辨率除以矩形组件分辨率得到布局板边上能放置组件数目
    amount_in_side = int(board_grid / unit_grid)
    # 创建布局矩阵
    layout_array = np.zeros(shape=(board_grid, board_grid), dtype=np.int)
    for position in positions:
        # 计算每个组件最左下角像素的坐标，由最左下角坐标依次在组件分辨率范围内赋值，使有组件部位整块都表示为“1”
        # 注意：最后一列为特殊情况，区分对待
        # 注意：坐标索引从0开始
        hang = position // amount_in_side
        lie = position % amount_in_side
        if lie >= 1:
            lie -= 1

        else:
            hang -= 1
            lie = amount_in_side - 1

        for i in range(unit_grid):
            for j in range(unit_grid):
                layout_array[hang * unit_grid + i, lie * unit_grid + j] = 1

    return layout_array
