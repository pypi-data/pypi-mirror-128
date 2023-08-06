
# TODO 正确导入函数 generate_matrix, save_matrix, save_fig
from cli import get_options  # TODO: 保证不修改本行也可以正确导入
from generator.core import generate_matrix
from generator.utils import save_matrix, save_fig, make_dir


def main():

    args = get_options()
    board_grid = args.board_grid
    unit_grid = args.unit_grid

    if board_grid % unit_grid != 0:
        exit()

    unit_n = args.unit_n
    positions = args.positions
    if len(positions) == unit_n:
        limit = (board_grid/unit_grid)**2

        for i in positions:

            print(i)
            if i < 1 or i > limit:
                exit()
    else:
        exit()

    file_name = args.file_name
    outdir = args.outdir
    matrix = generate_matrix(board_grid, unit_grid, unit_n, positions)
    make_dir(outdir)
    file_name = outdir + '/' + file_name
    save_matrix(matrix, file_name)
    save_fig(matrix, file_name)
    # raise NotImplementedError  # TODO 使用导入的函数按命令行参数生成数据，包括 mat 文件与 jpg 文件


#if __name__ == "__main__":
#    main()
