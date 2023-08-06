"""
辅助函数
"""

# from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio
import os


def save_matrix(matrix, file_name):
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    a = file_name + '.mat'
    sio.savemat(a, {'matrix': matrix})
    # raise NotImplementedError


def save_fig(matrix, file_name):
    # TODO: 将 matrix 画图保存到 file_name.jpg
    plt.imshow(matrix)
    a = file_name + '.jpg'
    plt.savefig(a)
    # /raise NotImplementedError


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    isExists = os.path.exists(outdir)
    if not isExists:
        os.makedirs(outdir)
    return outdir
    # raise NotImplementedError
