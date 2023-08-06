"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    sio.savemat(file_name + '.mat', {'matrix': matrix})


def save_fig(matrix, file_name):
    plt.imshow(matrix)
    plt.savefig(file_name + '.jpg')


def make_dir(outdir):
    Path(outdir).mkdir(parents=True, exist_ok=True)
