import argparse


def get_options():
    parser = argparse.ArgumentParser(
        description="simple layout parameters")
    parser.add_argument(
        '--board_grid',
        type=int,
        default=100,
        # required=True,
        help="The resoultion of plane, width/length of rectangle")
    parser.add_argument(
        '--unit_grid',
        type=int,
        default=10,
        # required=True,
        help="The resoultion of component")
    parser.add_argument(
        '--unit_n',
        type=int,
        default=3,
        # required=True,
        help="Number of component")
    parser.add_argument(
        '--positions',
        type=int,
        nargs='+',
        default=[1, 15, 33],
        # required=True,
        help="Position of component")
    parser.add_argument(
        '--outdir', '-o',
        type=str,
        default='./',
        help="The save path of output")
    parser.add_argument(
        '--file_name',
        type=str,
        # required=True,
        default='example',
        help="file name")
    options = parser.parse_args()
    return options
