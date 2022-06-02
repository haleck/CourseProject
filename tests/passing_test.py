from unittest import TestCase, main
from passing import *


class PassingTest(TestCase):
    def test_def_leader(self):
        executor = MazeSolver(max_population=1)
        maze = Maze()
        executor.set_maze(maze)
        executor.set_population(Population(maze))
        leader = executor.define_leader()
        executor.fitnessValues = [individual.individual_fitness for individual in executor.get_population()]
        self.assertEqual(leader, min(executor.get_population(), key=lambda indi: indi.individual_fitness))


if __name__ == '__main__':
    main()
