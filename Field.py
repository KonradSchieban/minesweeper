from random import randint


class Field():

    def __init__(self, num_cols, num_rows, num_mines):

        self._num_cols = num_cols
        self._num_rows = num_rows

        self._field = []

        for row_index in range(num_rows):
            row = [0] * num_cols
            self._field.append(row)

        mine_coords = [None] * num_mines
        for i in range(num_mines):

            mine_col = randint(0,num_cols-1)
            mine_row = randint(0,num_rows-1)
            new_mine = [mine_row, mine_col]
            while new_mine in mine_coords:
                mine_col = randint(0,num_cols-1)
                mine_row = randint(0,num_rows-1)
                new_mine = [mine_row, mine_col]
            mine_coords[i] = new_mine
 
        for mine in mine_coords:
            row = self._field[mine[0]]
            row[mine[1]] = 1
        
        return

    def get_num_rows(self):
        return self._num_rows

    def get_num_cols(self):
        return self._num_cols

    def cell_is_bomb(self, row, col):
        return self._field[row][col] == 1

    def in_bounds(self, row, col):
        return row >= 0 and row < self._num_rows and col >= 0 and col < self._num_cols

    def get_num_adjacent_bombs(self, row, col):

        num_adj_bombs = 0
        
        d_col = -1
        while d_col < 2:
            d_row = -1
            while d_row < 2:
                if self.in_bounds(row + d_row, col + d_col):
                    if self.cell_is_bomb(row + d_row, col + d_col):
                        num_adj_bombs += 1
                d_row += 1
            d_col += 1

        return num_adj_bombs

    def render(self):
       
        init_str = '|'
        for col_index in range(self._num_cols):
            init_str += '-'
        init_str += '|'
        print(init_str)

        for row_index in range(self._num_rows):
            row_str = "|"
            for col_index in range(self._num_cols):
                row_str += str(self._field[row_index][col_index])
            row_str += '|'
            print(row_str)

        print(init_str)

        return


if __name__ == '__main__':
    field = Field(50,20,14)
    field.render()


