"""
辅助函数
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    sio.savemat(Path(file_name).with_suffix(".mat"), {"matrix": matrix})


def save_fig(matrix, file_name):
    plt.imsave(Path(file_name).with_suffix(".jpg"), matrix)


def make_dir(outdir):
    if not Path(outdir).exists():
        os.makedirs(outdir)
