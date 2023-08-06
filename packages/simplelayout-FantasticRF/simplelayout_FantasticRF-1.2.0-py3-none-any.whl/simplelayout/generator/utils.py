"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    mdict = {"matrix": matrix, 'label': 'unit_layout'}
    path = file_name + '.mat'
    sio.savemat(path, mdict)


def save_fig(matrix, file_name):
    plt.imshow(matrix)
    path = file_name + '.jpg'
    plt.savefig(path)


def make_dir(outdir):
    Path(outdir).mkdir(parents=True, exist_ok=True)
