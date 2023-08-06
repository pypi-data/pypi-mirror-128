# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli.cli_generate import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix
from simplelayout.generator.utils import save_fig
from simplelayout.generator.utils import make_dir


def main():
    # raise NotImplementedError  # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件
    Right_options = get_options()
    data = generate_matrix(board_grid=Right_options.board_grid,
                           unit_grid=Right_options.unit_grid,
                           unit_n=Right_options.unit_n,
                           positions=Right_options.positions)
    outdir = make_dir(Right_options.outdir)     # 创建结果目录
    filepath = outdir + "/" + Right_options.file_name   # 在创建的目录下创建文件路径
    save_matrix(data, filepath)
    # TODO: 存储 matrix 到 file_name.mat, mdict 的 key 为 "matrix"
    save_fig(data, filepath)
    # TODO: 将 matrix 画图保存到 file_name.jpg


if __name__ == "__main__":
    main()
