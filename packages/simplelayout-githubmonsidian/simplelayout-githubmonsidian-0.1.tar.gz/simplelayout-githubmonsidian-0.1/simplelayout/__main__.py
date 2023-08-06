# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from simplelayout.cli import get_options  # TODO: 保证不修改本行也可以正确导入
from simplelayout.generator.utils import save_matrix, save_fig, make_dir
from simplelayout.generator.core import generate_matrix


def main():
    options = get_options()
    m = generate_matrix(options.board_grid,
                        options.unit_grid, options.unit_n, options.positions)
    outDir = options.outdir
    make_dir(outDir)
    fileName = options.file_name
    path = outDir + '/' + fileName
    save_matrix(m, path)
    save_fig(m, path)
    return
    raise NotImplementedError  # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件


if __name__ == "__main__":
    main()
