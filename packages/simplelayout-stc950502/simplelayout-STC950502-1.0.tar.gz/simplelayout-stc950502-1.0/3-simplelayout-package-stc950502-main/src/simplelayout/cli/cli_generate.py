import argparse
import os
import sys

def get_options():
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_grid', type=int)
    parser.add_argument('--unit_grid', type=int)
    parser.add_argument('--unit_n', type=int)
    parser.add_argument('--positinons', type=int, nargs = '+')
    parser.add_argument('--outdir', type=str)
    parser.add_argument('--file_name', type=str)
    options = parser.parse_args()
    if options.board_grid % options.unit_grid or len(options.positions) != options.unit_n:
        sys.exit()
    for i in options.positions:
        if i < 1 or i > (options.board_grid / options.unit_grid) ** 2:
            sys.exit()
    path = options.outdir
    if not os.path.exists(path):
        os.makedirs(path)
    return 
