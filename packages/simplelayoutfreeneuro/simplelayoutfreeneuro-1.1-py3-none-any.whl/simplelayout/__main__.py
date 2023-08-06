from simplelayout.cli import get_options
from simplelayout.generator import core, utils
from pathlib import Path


def main():
    args = get_options()
    board = core.generate_matrix(args.board_grid, args.unit_grid, args.unit_n,
                                 args.positions)
    filename = Path(args.outdir) / args.file_name
    utils.make_dir(Path(args.outdir))
    utils.save_fig(board, filename)
    utils.save_matrix(board, filename)


if __name__ == "__main__":
    main()
