import argparse


def get_options():
    parser = argparse.ArgumentParser(description='Third Homework')
    parser.add_argument('--board_grid', type=int, help='布局板分辨率')
    parser.add_argument('--unit_grid', type=int, help='矩形组件分辨率')
    parser.add_argument('--unit_n', type=int, help='组件数')
    parser.add_argument('--positions', nargs='+', type=int)
    parser.add_argument('--outdir', type=str, help='输出结果的目录')
    parser.add_argument('--file_name', type=str, help='输出文件名')
    options = parser.parse_args()
    return options
