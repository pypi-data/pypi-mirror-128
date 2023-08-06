"""
数据生成的主要逻辑
"""

import numpy as np
# from numpy.matrixlib.defmatrix import matrix


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
    n = int(board_grid / unit_grid)
    matrix_a = np.zeros((n, n))
    matrix_a = matrix_a.astype(int)
    matrix_b = np.ones((unit_grid, unit_grid))
    matrix_b = matrix_b.astype(int)
    ll = len(positions)
    for i in range(0, ll):
        a = positions[i] % n
        b = positions[i] // n
        if a == 0:
            matrix_a[b-1][n-1] = 1
        else:
            matrix_a[b][a-1] = 1
    matrix_c = np.kron(matrix_a, matrix_b)
    return matrix_c
    # raise NotImplementedError  # TODO: 实现布局矩阵的生成
