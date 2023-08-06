"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    mdict = {'matrix': matrix, 'label': 'layout_array'}
    sio.savemat(file_name + '.mat', mdict)


def save_fig(matrix, file_name):
    # TODO: 将 matrix 画图保存到 file_name.jpg
    plt.imshow(matrix)
    plt.savefig(file_name + '.jpg')


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    path = Path(outdir)
    path.mkdir(parents=True, exist_ok=True)
