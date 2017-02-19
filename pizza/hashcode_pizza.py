import pprint
import sys

TOMATOS = 'T'
MUSHROOMS = 'M'


class Cell:
    def __init__(self, i, j, cell_type, pizza):
        self.i = i
        self.j = j
        self.cell_type = cell_type
        self.cells = pizza.pizza_matrix
        self.rows = pizza.rows
        self.columns = pizza.columns
        self.min_ingredients = pizza.min_ingredients
        self.max_slices = pizza.max_slices
        self.dirty = False
        self.dirtyIndex = 0

    def __str__(self):
        return 'i={} j={} cell_type={}'.format(self.i, self.j, self.cell_type)

    def __repr__(self):
        return 'd{}'.format(self.dirtyIndex) if self.dirty else '{}'.format(self.cell_type)

    def find_matches(self):
        return {
            'right': self.get_right(),
            'left': self.get_left(),
            'top': self.get_top(),
            'bottom': self.get_bottom()
        }

    def _check_condition(self, total_counter, t_count, m_count, is_cell_used):

        return all([total_counter < self.max_slices,
                    (bool(t_count) | bool(m_count) or t_count == m_count == 0),
                    not is_cell_used])

    def get_bottom(self):
        ing_map = {'T': 0, "M": 0}
        counter = 0
        start = min(self.i,  self.rows)
        for row in range(start, self.rows):
            next_cell = self.cells[row][self.j]
            if self._check_condition(counter, ing_map.get('T'), ing_map.get('M'),
                                     next_cell.dirty):
                ing_map[next_cell.cell_type] += 1
                counter += 1
            else:
                break
        return counter

    def get_top(self):
        ing_map = {'T': 0, "M": 0}
        counter = 0
        start = max(self.i, 0)
        for row in range(start, 0, -1):
            next_cell = self.cells[row][self.j]
            if self._check_condition(counter, ing_map.get('T'), ing_map.get('M'),
                                     next_cell.dirty):
                ing_map[next_cell.cell_type] += 1
                counter += 1
            else:
                break
        return counter

    def get_right(self):
        ing_map = {'T': 0, "M": 0}
        counter = 0
        start = max(self.j, 0)
        for cell in range(start, 0, -1):
            next_cell = self.cells[self.i][cell]
            if self._check_condition(counter, ing_map.get('T'), ing_map.get('M'),
                                     next_cell.dirty):
                ing_map[next_cell.cell_type] += 1
                counter += 1
            else:
                break
        return counter

    def get_left(self):
        ing_map = {'T': 0, "M": 0}
        counter = 0
        start = min(self.j, self.columns)
        for cell in range(start, self.columns):
            next_cell = self.cells[self.i][cell]
            if self._check_condition(counter, ing_map.get('T'), ing_map.get('M'),
                                     next_cell.dirty):
                ing_map[next_cell.cell_type] += 1
                counter += 1
            else:
                break
        return counter


class PizzaTile(object):
    def __init__(self, i1, j1, i2, j2, pizza_matrix, max_slices, min_ingredients):
        self.i1 = i1
        self.i2 = i2
        self.j1 = j1
        self.j2 = j2
        self.pizza_matrix = pizza_matrix
        self.max_slices = max_slices
        self.min_ingredients = min_ingredients

    def __str__(self):
        return 'j1={} j2={} i1={} i2={}'.format(self.j1, self.j2, self.i1, self.i2)

    def get_slices(self):
        return (abs(self.j1 - self.j2) +1) * (abs(self.i1 - self.i2) + 1)

    def validate_tile(self):
        if self.get_slices() > self.max_slices:
            return False
        return True if self.count_type(TOMATOS) >= self.min_ingredients and self.count_type(
            MUSHROOMS) >= self.min_ingredients else False

    def count_type(self, cell_type):
        counter = 0
        for row in range(min(self.i1, self.i2), max(self.i1, self.i2) +1):
            for column in range(min(self.j1, self.j2), max(self.j1, self.j2) +1):
                if self.pizza_matrix[row][column].cell_type == cell_type:
                    counter += 1
        return counter

    def mark_dirty(self, dirty_index):
        for row in range(min(self.i1, self.i2), max(self.i1, self.i2) +1):
            for column in range(min(self.j1, self.j2), max(self.j1, self.j2) +1):
                self.pizza_matrix[row][column].dirtyIndex = dirty_index
                self.pizza_matrix[row][column].dirty = True

class Pizza(object):

    def __init__(self, rows, columns, min_per_slice, max_cells_in_slice):
        self.tiles = []
        self.pizza_matrix = [[0 for y in xrange(columns)] for x in xrange(rows)]
        pprint.pprint(self.pizza_matrix)
        self.rows = rows
        self.columns = columns
        self.max_slices = max_cells_in_slice
        self.min_ingredients = min_per_slice

    def permutations(self):
        return [(2, 2), (3, 4), (4, 3), (1, 12), (12, 1), (6, 2), (2, 6)]

    def get_sorted_cells(self):
        sorted_cells = []
        dirty_index = 1
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.pizza_matrix[row][column]
                result = cell.find_matches()
                r = result.get('right')
                l = result.get('left')
                t = result.get('top')
                b = result.get('bottom')
                tile = None
                if l == self.max_slices:
                    tile = PizzaTile(cell.i, cell.j, cell.i, cell.j + 4,
                                     self.pizza_matrix,
                                     self.max_slices,
                                     self.min_ingredients)
                elif r == self.max_slices:
                    tile = PizzaTile(cell.i, cell.j, cell.i, cell.j - 4,
                                     self.pizza_matrix,
                                     self.max_slices,
                                     self.min_ingredients)
                elif b == self.max_slices:
                    tile = PizzaTile(cell.i, cell.j, cell.i+4, cell.j,
                                     self.pizza_matrix,
                                     self.max_slices,
                                     self.min_ingredients)
                elif t == self.max_slices:
                    tile = PizzaTile(cell.i, cell.j, cell.i-4, cell.j,
                                     self.pizza_matrix,
                                     self.max_slices,
                                     self.min_ingredients)

                if tile and tile.validate_tile():
                    tile.mark_dirty(dirty_index)
                    dirty_index += 1
                    sorted_cells.append(tile)
                    pprint.pprint(self.pizza_matrix)


def read_file(filename):
    with open(filename, 'r') as f_file:
        header_conf = [int(num) for num in f_file.readline().split()]
        _pizza = Pizza(*header_conf)
        # read matrix
        for row in range(_pizza.rows):
            str_line = f_file.readline().strip()
            columns = list(str_line)
            for column in range(len(columns)):
                _pizza.pizza_matrix[row][column] = Cell(row, column, columns[column], _pizza)

        pprint.pprint(_pizza.pizza_matrix)
        _pizza.get_sorted_cells()
        return _pizza


if __name__ == '__main__':
    pizza = read_file('pizza/small.in')