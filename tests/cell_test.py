from unittest import TestCase, main
from generator import *
from settings import *


class CellTest(TestCase):
    def test_cell_finding(self):
        self.assertEqual(Cell.find_index(100, 100), 100+100*cols)

    def test_negative_coords_cell(self):
        with self.assertRaises(TypeError) as e:
            Cell(-1, 21)
        self.assertEqual('Координаты клетки не могут быть отрицательными числами', e.exception.args[0])

        with self.assertRaises(TypeError) as e:
            Cell(21, -1)
        self.assertEqual('Координаты клетки не могут быть отрицательными числами', e.exception.args[0])

    def test_unreal_coords(self):
        cell = Cell(10, 21)

        self.assertEqual(cell.check_cell(-1, 2), False)
        self.assertEqual(cell.check_cell(10000, 1), False)

    def test_maze_not_created(self):
        cell = Cell(10, 21)

        with self.assertRaises(AttributeError) as e:
            cell.check_cell(1, 1)
        self.assertEqual('Не задано поле лабиринта', e.exception.args[0])

    def test_return_of_check_neighbors(self):
        cell = Cell(0, 0)

        grid_cells = [Cell(col, row) for row in range(30) for col in range(30)]
        cell.grid_cells = grid_cells

        neighbors = cell.check_neighbors(grid_cells)
        self.assertEqual(neighbors, grid_cells[Cell.find_index(1, 0)] if neighbors.x == 1 else grid_cells[Cell.find_index(0, 1)])


if __name__ == '__main__':
    main()
