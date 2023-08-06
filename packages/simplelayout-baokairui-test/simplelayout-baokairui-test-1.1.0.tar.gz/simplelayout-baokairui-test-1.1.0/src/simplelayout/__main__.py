# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_matrix
from simplelayout.generator.utils import save_fig
from simplelayout.generator.utils import make_dir


def main():
    # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件
    option = get_options()
    image = generate_matrix(
        option.board_grid, option.unit_grid, option.unit_n, option.positions)
    make_dir(option.outdir)
    file_path = '{}/{}'.format(option.outdir, option.file_name)
    save_matrix(image, file_path)
    save_fig(image, file_path)


if __name__ == "__main__":
    main()
