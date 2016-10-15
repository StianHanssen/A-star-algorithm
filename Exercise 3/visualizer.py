from PIL import Image, ImageDraw
from board import Board
import os


color_dict = {'.': '#ffffff', '#': '#000000', 'A': '#ff0000', 'B': '#b5871c',
              'w': '#1c9bb5', 'm': '#8a989b', 'f': '#1f7a37', 'g': '#4bbc00',
              'r': '#af710c'}

def draw_board(board, opened, closed, save_name=None):
    cell_dim = 50
    ratio = 1/5.5
    offset = cell_dim * ratio
    inv_offset = cell_dim * ((1 - ratio) - ratio)
    canvas = (board.WIDTH * cell_dim, board.HEIGHT * cell_dim)
    im = Image.new('RGBA', canvas, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    path = board.get_path()
    text = list(Board.clean_up(board.BOARD_STR))
    for y in range(board.HEIGHT):
        for x in range(board.WIDTH):
            color = color_dict[text[x + y * board.WIDTH]]
            x1, y1 = x * cell_dim, y * cell_dim
            x2, y2 = (x + cell_dim) * cell_dim, (y + cell_dim) * cell_dim
            draw.rectangle([x1, y1, x2, y2], fill=color)
    if closed is not None:
        closed -= {board.START, board.END}
        for c in closed:
            color = '#00BCD4'
            draw.ellipse(calc_circle(c.X, c.Y, cell_dim, offset, inv_offset), fill=color)
    if opened is not None:
        opened = set(opened)
        opened -= {board.START, board.END}
        for c in opened:
            color = '#006064'
            draw.ellipse(calc_circle(c.X, c.Y, cell_dim, offset, inv_offset), fill=color)
    for x, y in path:
        color = '#DD2C00'
        draw.ellipse(calc_circle(x, y, cell_dim, offset, inv_offset), fill=color)
    im.show()
    if save_name is not None:
        im.save(get_file_path(save_name))

def calc_rectangle(x, y, cell_dim):
    x1, y1 = x * cell_dim, y * cell_dim
    x2, y2 = (x + cell_dim) * cell_dim, (y + cell_dim) * cell_dim
    return [x1, y1, x2, y2]

def calc_circle(x, y, cell_dim, offset, inv_offset):
    x1, y1 = (x * cell_dim) + offset, (y * cell_dim) + offset
    x2, y2 = x1 + inv_offset, y1 + inv_offset
    return [x1, y1, x2, y2]

def get_file_path(file_name, mac=False):
    """Gets file path to given file_name, which has to be in the folder boards
    Args:
        file_name (str): Name of the txt we want to import a board from
        mac (bool): If True will work for mac, works for windows otherwise

    Returns:
        A string being the file path to the given filename.
    """
    folder = "/paths/" if mac else "\\paths\\"
    path = os.path.dirname(os.path.abspath(__file__))
    path += folder + file_name
    return path
