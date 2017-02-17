import pprint
import sys

TOMATOS = 'T'
MUSHROOMS = 'M'


class Cell:
    def __init__(self, i, j, cell_type, cells, pizza_tiles):
        self.i = i
        self.j = j
        self.cell_type = cell_type
        self.cells = cells
        self.pizza_tiles = pizza_tiles

    def __str__(self):
        return 'i={} j={} cell_type={}'.format(self.i, self.j, self.cell_type)

    @property
    def similar_neightbors(self):
        return {
            'right': self.get_right(),
            'left': self.get_left(),
            'top': self.get_top(),
            'bottom': self.get_bottom()
        }

    @property
    def dirty(self):
        for tile in pizza_tiles:
            if self.i in range(max(tile.x1, tile.x2)) and self.j in range(max(tile.y1, tile.y2)):
                return True
        return False


    def get_bottom(self):
        step = 1
        counter = 0
        while True:
            try:
                neighboor = self.cells[self.i + step + counter, self.j]
            except IndexError:
                break
            if self.cell_type == neighboor.cell_type and not neighboor.dirty:
                counter += 1
            else:
                break
        return abs(counter)

    def get_top(self):
        step = 1
        counter = 0
        while True:
            try:
                neighboor = self.cells[self.i - step - counter][self.j]
            except IndexError:
                break
            if self.cell_type == neighboor.cell_type and not neighboor.dirty:
                counter -= 1
            else:
                break
        return abs(counter)

    def get_left(self):
        step = 1
        counter = 0
        while True:
            try:
                neighboor = self.cells[self.i][self.j - step - counter]
            except IndexError:
                break
            if self.cell_type == neighboor.cell_type and not neighboor.dirty:
                counter -= 1
            else:
                break
        return abs(counter)

    def get_right(self):
        step = 1
        counter = 0
        while True:
            try:
                neighboor = self.cells[self.i][self.j + step + counter]
            except IndexError:
                break
            if self.cell_type == neighboor.cell_type and not neighboor.dirty:
                counter -= 1
            else:
                break
        return abs(counter)


class PizzaTile(object):
    def __init__(self, y1, x1, y2, x2, pizza_matrix, max_slices, min_ingredients):
        self.y1 = y1
        self.y2 = y2
        self.x1 = x1
        self.x2 = x2
        self.pizza_matrix = pizza_matrix
        self.max_slices = max_slices
        self.min_ingredients = min_ingredients

    def __str__(self):
        return 'y1={} y2={} x1={} x2={}'.format(self.x1, self.x2, self.y1, self.y2)

    def get_slices(self):
        return (abs(self.x1 - self.x2) + 1) * (abs(self.y1 - self.y2) + 1)

    def validate_tile(self):
        if self.get_slices() > self.max_slices:
            return False

        tomatos = self.count_type(TOMATOS)
        if tomatos < self.min_ingredients:
            return False
        mushrooms = self.count_type(MUSHROOMS)
        if mushrooms < self.min_ingredients:
            return False

    def count_type(self, cell_type):
        counter = 0
        for row in range(max(self.x1, self.x2), min(self.x1, self.x2)):
            for column in range(max(self.y1, self.y2), min(self.y1, self.y2)):
                if self.pizza_matrix[row][column].cell_type == cell_type:
                    counter += 1
        return counter


class Pizza(object):

    def __init__(self, rows, columns, min_per_slice, max_cells_in_slice):
        self.tiles = []
        self.pizza_matrix = [[0 for y in xrange(columns)] for x in xrange(rows)]
        pprint.pprint(self.pizza_matrix)
        self.rows = rows
        self.columns = columns
        self.min_per_slice = min_per_slice
        self.max_cells_in_slice = max_cells_in_slice

    def get_max_cardinality_cell(self):
        pass
        # for row in xrange(self.pizza_matrix):
        #     for column in se


def read_file(filename):
    with open(filename, 'r') as f_file:
        header_conf = [int(num) for num in f_file.readline().split()]
        _pizza = Pizza(*header_conf)
        # read matrix
        pizza_tiles = []
        for row in range(_pizza.rows):
            str_line = f_file.readline().strip()
            columns = list(str_line)
            for column in range(len(columns)):
                _pizza.pizza_matrix[row][column] = Cell(row, column, columns[column], _pizza.pizza_matrix, pizza_tiles)

        pprint.pprint(_pizza.pizza_matrix)
        return _pizza


if __name__ == '__main__':
    pizza = read_file('small.in')