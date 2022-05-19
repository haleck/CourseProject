from unittest import TestCase, main
from generator import *
from settings import *


class MazeTest(TestCase):
    def test_all_cells_contains_exit(self):
        maze = Maze()
        self.assertEqual(all([any([not cell.walls.get(side) for side in ['left', 'right', 'bottom', 'top']]) for cell in maze.grid_cells]), True)

    def test_call_maze(self):
        maze = Maze()
        self.assertEqual(isinstance(maze(), list), True)

    def test_del_cell(self):
        maze = Maze()
        chosen_cell = choice(maze())
        x, y = chosen_cell.x, chosen_cell.y
        del maze[Cell.find_index(x, y)]
        self.assertEqual(all([(cell.x, cell.y) != (x, y) for cell in maze()]), True)

if __name__ == '__main__':
    main()
