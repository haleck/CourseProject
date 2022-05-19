from unittest import TestCase, main
from genetic import *


class MazeTest(TestCase):
    def test_choose_next(self):
        pairs = []
        maze = Maze()
        ind = Individual(maze.grid_cells)
        for i in range(len(ind.maze)):
            (past_cell, new_cell) = ind.current_cell, ind.choose_next()
            pairs.append((past_cell, new_cell))
            ind.move_to(new_cell, add=False)
        self.assertEqual(all(new_cell.x - past_cell.x <= 1 and new_cell.y - past_cell.y <= 1 for (past_cell, new_cell) in pairs), True)


if __name__ == '__main__':
    main()
