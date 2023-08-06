from simplelayout.cli import get_options
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix, save_fig, make_dir


def main():
    options = get_options()
    unit_layout = generate_matrix(
        options.board_grid,
        options.unit_grid,
        options.unit_n,
        options.positions)
    make_dir(options.outdir)
    full_path = options.outdir+'/'+options.file_name
    save_matrix(unit_layout, full_path)
    save_fig(unit_layout, full_path)


if __name__ == "__main__":
    main()
