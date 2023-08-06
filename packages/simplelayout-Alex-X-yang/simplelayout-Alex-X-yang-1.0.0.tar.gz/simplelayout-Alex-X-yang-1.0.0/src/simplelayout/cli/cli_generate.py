import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser = argparse.ArgumentParser(description='Creat files.')
    parser.add_argument('--board_grid', type=int, default=100)
    parser.add_argument('--unit_grid', type=int, default=10)
    parser.add_argument('--unit_n', type=int, default=3)
    parser.add_argument('--positions', type=int,
                        default=[1, 15, 33], nargs='+')
    parser.add_argument('-o', '--outdir', type=str, default='dir1/dir2')
    parser.add_argument('--file_name', type=str, default='example')

    options = parser.parse_args()

    # board_grid整除unit_grid，否则退出
    if options.board_grid % options.unit_grid != 0:
        sys.exit(0)

    # positions数量与unit_n一致
    # 从1开始的整数，上限为(board_grid/unit_grid)^2
    # 若不满足要求退出程序
    if len(options.positions) == options.unit_n:
        for i in options.positions:
            if i >= 1 and i <= (options.board_grid / options.unit_grid) ** 2:
                continue
    else:
        sys.exit(0)
    return options
