"""
辅助函数
"""

from pathlib import Path
import matplotlib.pyplot as plt
import scipy.io as sio


def save_matrix(matrix, file_name):
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    sio.savemat("{}.{}".format(file_name, 'mat'), {"matrix": matrix})


def save_fig(matrix, file_name):
    # TODO: 将 matrix 画图保存到 file_name.jpg
    plt.imsave("{}.{}".format(file_name, 'jpg'), matrix, cmap="gray")
    plt.imshow(matrix)
    plt.show()


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    if not Path(outdir).exists():  # 判断目录是否存在
        Path(outdir).mkdir(parents=True, exist_ok=True)
