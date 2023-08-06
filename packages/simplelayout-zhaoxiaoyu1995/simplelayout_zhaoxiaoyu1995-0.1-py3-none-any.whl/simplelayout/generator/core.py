"""
数据生成的主要逻辑
"""

import numpy as np


def generate_matrix(board_grid: int, unit_grid: int, unit_n: int,
                    positions: list) -> np.ndarray:
    """生成指定布局矩阵

    Args:
        board_grid (int): 布局板分辨率，代表矩形区域的边长像素数
        unit_grid (int): 矩形组件分辨率
        unit_n (int): 组件数
        positions (list): 每个元素代表每个组件的位置
    Returns:
        np.ndarray: 布局矩阵
    """
    # layout = np.zeros((board_grid, board_grid))
    interval = int(board_grid / unit_grid)
    sequences = np.zeros(interval**2)
    sequences[np.array(positions) - 1] = 1
    layout = np.kron(sequences.reshape(interval, interval),
                     np.ones((unit_grid, unit_grid)))
    # for pos in positions:
    #     raw = int(math.floor((pos - 1) / interval))
    #     col = int((pos - 1) % interval)
    #     layout[
    #         (raw * unit_grid):(raw * unit_grid + unit_grid),
    #         (col * unit_grid):(col * unit_grid + unit_grid)
    #     ] = np.ones((unit_grid, unit_grid))
    return layout
