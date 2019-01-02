#!/usr/local/bin/python3
import sys
from Field import Field
from queue import Queue


class MineSweeper():

    def __init__(self, num_cols, num_rows, num_mines):

        self._num_cols = num_cols
        self._num_rows = num_rows

        self._field = Field(num_cols, num_rows, num_mines)

        self._image = []
        for row_index in range(num_rows):
            row = ['?'] * num_cols
            self._image.append(row)

        self.flags_used = 0

    def in_bounds(self, row, col):
        return row >= 0 and row < self._num_rows and col >= 0 and col < self._num_cols

    def get_image(self):
        return self._image

    def render(self):
   
        init_str = '|'
        for col_index in range(self._num_cols):
            init_str += '-'
        init_str += '|'
        print(init_str)

        for row_index in range(self._num_rows):
            row_str = "|"
            for col_index in range(self._num_cols):
                row_str += str(self._image[row_index][col_index])
            row_str += '|'
            print(row_str)

        print(init_str)

        return

    def test_cell_rec(self, row, col):
        if not self._field.cell_is_bomb(row, col):
            num_adjacent_bombs = self._field.get_num_adjacent_bombs(row,col)
            self._image[row][col] = num_adjacent_bombs

            if num_adjacent_bombs == 0:
                d_col = -1
                while d_col < 2:
                    d_row = -1
                    while d_row < 2:
                        if row + d_row >= 0 and row + d_row < self._num_rows and col + d_col >= 0 and col + d_col < self._num_cols:
                            if self._image[row + d_row][col + d_col] == '?':
                                self.test_cell_rec(row + d_row, col + d_col)
                        d_row += 1
                    d_col += 1

            return True

        else:
            self._image[row][col] = 'X'
            return False

    def test_cell_iter(self, row, col):
        if not self._field.cell_is_bomb(row, col):
            cell_queue = Queue()
            cell_queue.put([row, col])

            traveled_coords = []

            while not cell_queue.empty():
                cell_coords = cell_queue.get()
                row = cell_coords[0]
                col = cell_coords[1]

                if [row, col] in traveled_coords:
                    continue

                num_adjacent_bombs = self._field.get_num_adjacent_bombs(row, col)
                if num_adjacent_bombs == 0:
                    self._image[row][col] = ' '
                else:
                    self._image[row][col] = num_adjacent_bombs

                traveled_coords.append([row, col])

                if num_adjacent_bombs == 0:
                    d_col = -1
                    while d_col < 2:
                        d_row = -1
                        while d_row < 2:
                            if self.in_bounds(row + d_row, col + d_col):
                                if self._image[row + d_row][col + d_col] == '?':
                                    cell_queue.put([row + d_row, col + d_col])
                            d_row += 1
                        d_col += 1

            return True
        else:
            self._image[row][col] = 'X'
            return False

    def flag_cell(self, row, col):
        if self._image[row][col] == '?':
            self._image[row][col] = 'f'
            self.flags_used += 1
            return True
        else:
            return False

    def unflag_cell(self, row, col):
        if self._image[row][col] == 'f':
            self._image[row][col] = '?'
            self.flags_used -= 1
            return True
        else:
            return False

    def get_image_cell(self, row, col):
        return self._image[row][col]

    def get_flags_used(self):
        return self.flags_used


if __name__ == '__main__':

    do_prompt = True
    while do_prompt:
        try:
            num_cols = int(input("Enter number of columns for field: "))
            num_rows = int(input("Enter number of rows for field: "))
            num_mines = int(input("Enter number of mines: "))
            do_prompt = False
        except ValueError:
            print("Please only enter integers larger than zero!")

    mine_sweeper = MineSweeper(num_cols, num_rows, num_mines)
    mine_sweeper.render()

    is_playing = True
    while is_playing:
        try:
            col = int(input("Enter col: "))
            row = int(input("Enter row: "))
        except ValueError:
            print("Please enter only integers")

        is_playing = mine_sweeper.test_cell_iter(row, col)
        mine_sweeper.render()

    sys.exit(0)
