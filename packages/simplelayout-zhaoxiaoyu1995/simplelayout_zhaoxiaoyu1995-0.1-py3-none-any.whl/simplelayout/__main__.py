from simplelayout.cli import get_options
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix, save_fig, make_dir


def main():
    options = get_options()
    layout = generate_matrix(options.board_grid, options.unit_grid,
                             options.unit_n, options.positions)
    make_dir(options.outdir)
    save_matrix(layout, options.outdir + '/' + options.file_name)
    save_fig(layout, options.outdir + '/' + options.file_name)


if __name__ == "__main__":
    main()
