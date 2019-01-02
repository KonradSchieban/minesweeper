#!/usr/local/bin/python3
from tkinter import *
from MineSweeper import MineSweeper


class MineSweeperUI():

    def __init__(self, num_cols, num_rows, num_mines):

        self.mine_sweeper = MineSweeper(num_cols, num_rows, num_mines)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.line_distance = 25
        self.canvas_width = num_cols * self.line_distance
        self.canvas_height = num_rows * self.line_distance

        self.master = Tk()
        self.w = Canvas(self.master,
                        width=self.canvas_width,
                        height=self.canvas_height)

        self.w.bind("<Button-1>", self.left_click)
        self.w.bind("<Button-2>", self.right_click)
        self.text_box = Text(self.master, height=1, width=40)
        self.w.pack()
        self.text_box.pack()
        self.render_ui()

        mainloop()

    def left_click(self, event):
        col = event.x // self.line_distance
        row = event.y // self.line_distance
        if col < self.num_cols and row < self.num_rows:
            self.mine_sweeper.test_cell_iter(row, col)
            self.render_ui()

    def right_click(self, event):
        col = event.x // self.line_distance
        row = event.y // self.line_distance
        if self.mine_sweeper.get_image_cell(row, col) == 'f':
            self.mine_sweeper.unflag_cell(row, col)
        else:
            self.mine_sweeper.flag_cell(row, col)
        self.render_ui()

    def render_ui(self):

        # vertical lines at an interval of "line_distance" pixel
        for x in range(self.line_distance, self.canvas_width, self.line_distance):
            self.w.create_line(x, 0, x, self.canvas_height, fill="#476042")

        # horizontal lines at an interval of "line_distance" pixel
        for y in range(self.line_distance, self.canvas_height, self.line_distance):
            self.w.create_line(0, y, self.canvas_width, y, fill="#476042")

        image = self.mine_sweeper.get_image()

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if image[row][col] == '?':
                    fill_color = 'gray'
                elif image[row][col] == ' ':
                    fill_color = 'white'
                elif image[row][col] == 'f':
                    fill_color = 'red'
                else:
                    fill_color = 'yellow'

                self.w.create_rectangle(col*self.line_distance,
                                        row*self.line_distance,
                                        (col+1)*self.line_distance,
                                        (row+1)*self.line_distance, fill=fill_color)

                if not image[row][col] == '?' and not image[row][col] == ' ':
                    self.w.create_text(col * self.line_distance + self.line_distance // 2,
                                       row * self.line_distance + self.line_distance // 2,
                                       text=image[row][col])

        flags_text = "Flags used: " + str(self.mine_sweeper.flags_used)

        self.text_box.edit_undo()
        self.text_box.insert("current linestart", flags_text)


if __name__ == '__main__':
    ms_ui = MineSweeperUI(20, 12, 30)
