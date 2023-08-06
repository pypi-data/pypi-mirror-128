import matplotlib.pyplot as plt
import scipy.io as sio
import os


def save_matrix(matrix, file_name):
    sio.savemat(file_name+".mat", {'matrix': matrix})
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"


def save_fig(matrix, file_name):
    plt.imsave(file_name+".jpg", matrix)
    # TODO: 将 matrix 画图保存到 file_name.jpg


def make_dir(outdir):
    # TODO: 当目录 outdir 不存在时创建目录
    if not os.path.exists(outdir):
        os.makedirs(outdir)    # 当目录outdir不存在时创建目录
    return outdir
