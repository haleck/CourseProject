from settings import *
from generator import *
from random import choice, randint, random


class Individual:
    def __init__(self, maze):
        self.maze = maze
        self.current_cell = maze[0]
        self.current_index = 0
        self.stack = [maze[0]]
        self.route = 0
        self.individual_fitness = self.fitness()

    def fitness(self):
        return self.maze[FINISH].x - self.current_cell.x + self.maze[FINISH].y - self.current_cell.y + self.route * 0.1

    def choose_next(self):
        possible_cells = []
        found = False

        def check_availability(index):
            if self.stack and not self.maze[index] in self.stack:
                possible_cells.append(self.maze[index])
                return True
            elif self.stack and self.stack[-1] != self.maze[index]:
                possible_cells.append(self.maze[index])
                return True

        while not found:
            if not self.current_cell.walls['top']:
                if check_availability(self.current_index - cols):
                    found = True
            if not self.current_cell.walls['right']:
                if check_availability(self.current_index + 1):
                    found = True
            if not self.current_cell.walls['bottom']:
                if check_availability(self.current_index + cols):
                    found = True
            if not self.current_cell.walls['left']:
                if check_availability(self.current_index - 1):
                    found = True
            if not found:
                self.move_to(self.stack[-1])
                self.stack.pop()

        return choice(possible_cells)

    def move_to(self, next_cell: Cell, add=True, draw_the_way=False):
        if self.current_cell == self.maze[FINISH]:
            return
        if add:
            self.stack.append(self.current_cell)

        self.route += 1
        self.current_cell = next_cell
        self.current_index = next_cell.find_index(next_cell.x, next_cell.y)

    @staticmethod
    def draw_the_way(past_cell: Cell, current_cell: Cell, next_cell: Cell, color=(42, 168, 72)):
        x_past = past_cell.x * TILE
        y_past = past_cell.y * TILE
        x_current = current_cell.x * TILE
        y_current = current_cell.y * TILE
        x_next = next_cell.x * TILE
        y_next = next_cell.y * TILE

        coord_center = (x_current + TILE / 2, y_current + TILE / 2)
        coord_middle_right = (x_current + TILE, y_current + TILE/2)
        coord_middle_left = (x_current, y_current + TILE/2)
        coord_middle_top = (x_current + TILE /2, y_current)
        coord_middle_down = (x_current + TILE /2, y_current + TILE)

        if x_current - x_past == 1 * TILE:
            if y_current - y_next == 1 * TILE:
                pygame.draw.line(sc, color, coord_middle_left, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_top, 2)
                return
            if y_current - y_next == -1 * TILE:
                pygame.draw.line(sc, color, coord_middle_left, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_down, 2)
                return
            if x_past == x_next:
                return
            pygame.draw.line(sc, color, coord_middle_left, coord_middle_right, 2)
        elif x_current - x_past == -1 * TILE:
            if y_current - y_next == 1 * TILE:
                pygame.draw.line(sc, color, coord_middle_right, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_top, 2)
                return
            if y_current - y_next == -1 * TILE:
                pygame.draw.line(sc, color, coord_middle_right, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_down, 2)
                return
            if x_past == x_next:
                return
            pygame.draw.line(sc, color, coord_middle_right, coord_middle_left, 2)
        elif y_current - y_past == 1 * TILE:
            if x_current - x_next == 1 * TILE:
                pygame.draw.line(sc, color, coord_middle_top, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_left, 2)
                return
            if x_current - x_next == -1 * TILE:
                pygame.draw.line(sc, color, coord_middle_top, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_right, 2)
                return
            if y_past == y_next:
                return
            pygame.draw.line(sc, color, coord_middle_top, coord_middle_down, 2)
        elif y_current - y_past == -1 * TILE:
            if x_current - x_next == 1 * TILE:
                pygame.draw.line(sc, color, coord_middle_down, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_left, 2)
                return
            if x_current - x_next == -1 * TILE:
                pygame.draw.line(sc, color, coord_middle_down, coord_center, 2)
                pygame.draw.line(sc, color, coord_center, coord_middle_right, 2)
                return
            if y_past == y_next:
                return
            pygame.draw.line(sc, color, coord_middle_down, coord_middle_top, 2)


class Population:
    def __init__(self, maze):
        self.maze = maze
        self.individuals = [Individual(maze) for i in range(POPULATION_SIZE)]

    def clone(self, individual: Individual):
        new_fly = Individual(self.maze)
        new_fly.current_cell = individual.current_cell
        new_fly.stack[:] = individual.stack
        new_fly.individual_fitness = individual.individual_fitness
        new_fly.route = individual.route
        return new_fly

    @staticmethod
    def sel_tournament(population, p_len):
        offspring = []
        for n in range(p_len):
            i1 = i2 = i3 = 0
            while i1 == i2 or i1 == i3 or i2 == i3:
                i1, i2, i3 = randint(0, p_len - 1), randint(0, p_len - 1), randint(0, p_len - 1)

            offspring.append(
                min([population[i1], population[i2], population[i3]], key=lambda ind: ind.individual_fitness))

        return offspring

    @staticmethod
    def cx_two_points(child1: Individual, child2: Individual):
        size = min([len(child1.stack), len(child2.stack)])
        equal = []
        for i in range(size):
            if child2.stack[i] == child1.stack[i]:
                equal.append(i)
        if len(equal) >= 2:
            point1 = choice(equal)
            equal.remove(point1)
            point2 = choice(equal)
            equal.remove(point2)
            child1.stack[point1:point2], child2.stack[point1:point2] = child2.stack[point1:point2], child1.stack[
                                                                                                    point1:point2]

    def mut(self, mutant: Individual):
        if random() <= 0.2:
            a = mutant.stack[:randint(1, len(mutant.stack) - 1)]
            mutant.stack = a
            mutant.current_cell = mutant.stack[-1]
            mutant.current_index = Cell.find_index(mutant.current_cell.x, mutant.current_cell.y)
            return

        for count in range(3):
            index2 = False
            found = False
            index1 = randint(1, len(mutant.stack) - 1)
            element = mutant.stack[index1]
            if element == self.maze[FINISH]:
                break

            for i in range(0, len(mutant.stack) - 1):
                if mutant.stack[i] == element:
                    if found:
                        index2 = i
                        break
                    else:
                        found = True

            if index1 and index2:
                bug = 0
                if index2 < index1:
                    index1, index2 = index2, index1

                mutant_part_1 = mutant.stack[:index1]
                mutant_part_2 = mutant.stack[index2:]
                changed = False
                tempest = Individual(self.maze)
                tempest.stack = mutant_part_1
                tempest.current_cell = tempest.stack[-1]
                tempest.current_index = Cell.find_index(tempest.current_cell.x, tempest.current_cell.y)

                while not changed and bug < index2 - index1:
                    bug += 1
                    next_cell = tempest.choose_next()
                    tempest.move_to(next_cell)
                    if next_cell == element:
                        for i in range(len(mutant_part_2) - 1):
                            tempest.stack.append(mutant_part_2[i])
                        tempest.current_cell = tempest.stack[-1]
                        tempest.current_index = Cell.find_index(tempest.current_cell.x, tempest.current_cell.y)
                        changed = True

                if changed:
                    mutant.stack = tempest.stack
                    mutant.current_cell = tempest.current_cell
                    mutant.current_index = tempest.current_index



