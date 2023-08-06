import argparse
import os


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser.add_argument('--board_grid', type=int, default=100)
    parser.add_argument('--unit_grid', type=int, default=10)
    parser.add_argument('--unit_n', type=int, default=3)
    parser.add_argument('--positions', type=int, nargs='*')
    parser.add_argument('--outdir', type=str, default='example_dir')
    parser.add_argument('--file_name', type=str, default='example',)
    options = parser.parse_args()
    if options.board_grid % options.unit_grid != 0:
        os._exit(0)
        pass
    n = len(options.positions)
    if n != options.unit_n:
        os._exit(0)
        pass
    board = options.board_grid
    unit = options.unit_grid
    for i in range(0, n):
        if options.positions[i] < 1:
            os._exit(0)
            pass
        if options.positions[i] > (board / unit) ** 2:
            os._exit(0)
            pass
        pass
    return options
