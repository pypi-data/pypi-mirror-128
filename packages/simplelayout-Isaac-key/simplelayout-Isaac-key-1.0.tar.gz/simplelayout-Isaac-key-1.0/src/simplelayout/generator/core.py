"""
数据生成的主要逻辑
"""
import numpy as np
from numpy.matrixlib.defmatrix import matrix


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
    # 定义布局板矩阵
    matrix_board = np.zeros((board_grid, board_grid))

    # 定义单个组件矩阵
    matrix_unit = np.ones((unit_grid, unit_grid))

    # 定义单个矩形组件布局板中位置
    positions[:] = [x - 1 for x in positions]
    for i in range(0, unit_n):

        start_position_rows = int(
                                 (positions[i] // (board_grid / unit_grid))
                                 * unit_grid)
        start_position_cols = int(
                                (positions[i] % (board_grid / unit_grid))
                                * unit_grid)
        finish_position_rows = int(start_position_rows + unit_grid)
        finish_position_cols = int(start_position_cols + unit_grid)

        matrix_board[start_position_rows:finish_position_rows,
                     start_position_cols:finish_position_cols] = matrix_unit
        matrix(matrix_board)

    return matrix_board

    # raise NotImplementedError  # TODO: 实现布局矩阵的生成
