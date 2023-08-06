import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser(description='SimpleLAyout')
    parser.add_argument('--board_grid', type=int, default=100)
    parser.add_argument('--unit_grid', type=int, default=10)
    parser.add_argument('--unit_n', type=int, default=3)
    parser.add_argument('--positions', type=int,
                        nargs='*', default=[1, 15, 33])
    parser.add_argument('--outdir', '-o', type=str, default='dir1/dir2')
    parser.add_argument('--file_name', type=str, default='example')

    options = parser.parse_args()
    # 要求 board_grid 能整除 unit_grid
    if (options.board_grid % options.unit_grid) != 0:
        sys.exit()

    # positions数量与 unit_n 一致；
    # 位置为从1开始的整数，上限为 (board_grid/unit_grid)^2
    if len(options.positions) == options.unit_n:
        for pos in options.positions:
            if pos >= 1 and pos <= (options.board_grid/options.unit_grid)**2:
                continue
    else:
        sys.exit()
    return options
