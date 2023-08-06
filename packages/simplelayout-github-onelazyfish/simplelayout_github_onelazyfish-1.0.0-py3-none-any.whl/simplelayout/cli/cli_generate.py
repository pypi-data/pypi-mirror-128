import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser.add_argument("--board_grid", default=4, type=int,
                        help="Number of pixels")
    parser.add_argument("--unit_grid", default=2, type=int,
                        help="Rectangular component resolution")
    parser.add_argument("--unit_n", default=3, type=int,
                        help="Number of components")
    parser.add_argument("--positions", default=[1, 2, 4], type=int, nargs="+",
                        help="Location number of each component")
    parser.add_argument("-o", "--outdir", default="example_dir", type=str,
                        help="Directory of output file")
    parser.add_argument("--file_name", default="example", type=str,
                        help="Name of output file name")
    options = parser.parse_args()
    if options.board_grid % options.unit_grid != 0:
        sys.exit()
    if len(options.positions) > (options.board_grid / options.unit_grid) ** 2:
        sys.exit()
    if options.unit_n != len(options.positions):
        sys.exit()
    return options
