# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
import os
# import sys
# sys.path.append(".")
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix
from simplelayout.generator.utils import save_fig
from simplelayout.generator.utils import make_dir


def main():
    args = get_options()
    board = args.board_grid
    unit = args.unit_grid
    matrix = generate_matrix(board, unit, args.unit_n, args.positions)
    make_dir(args.outdir)
    os.chdir(args.outdir)
    save_matrix(matrix, args.file_name)
    save_fig(matrix, args.file_name)
    # raise NotImplementedError  # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件


if __name__ == "__main__":
    main()
