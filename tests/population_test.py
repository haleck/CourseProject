from unittest import TestCase, main
from genetic import *


class MazeTest(TestCase):
    def test_clone(self):
        maze = Maze()
        population = Population(maze)
        saved_ind = population.individuals[0]
        self.assertNotEqual(population.clone(saved_ind), saved_ind)

    def test_selection(self):
        population = Population(Maze())
        offspring = population.sel_tournament(population.individuals, len(population.individuals))
        self.assertEqual(len(offspring), len(population.individuals))

    def test_cx(self):
        ind1, ind2 = Individual(Maze()), Individual(Maze())
        ind1.stack, ind2.stack = [1, 6, 1, 1, 1, 6, 1], [2, 6, 2, 2, 2, 6, 2]
        Population.cx_two_points(ind1, ind2)
        self.assertEqual(ind2.stack, [2, 6, 1, 1, 1, 6, 2])


if __name__ == '__main__':
    main()
