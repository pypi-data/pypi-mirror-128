from simplelayout.cli import get_options  
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix
from simplelayout.generator.utils import save_fig
from simplelayout.generator.utils import make_dir


def main():
    options = get_options()
    layout_array = generate_matrix(
        options.board_grid,
        options.unit_grid,
        options.unit_n,
        options.positions,
    )
    make_dir(options.outdir)
    full_path = options.outdir+'/'+options.file_name
    save_matrix(layout_array, full_path)
    save_fig(layout_array, full_path)


if __name__ == "__main__":
    main()
