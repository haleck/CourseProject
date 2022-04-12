import pygame
from settings import *
from random import choice

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
pygame.display.set_caption('Они искали выход')


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def draw_current_cell(self, color=(42, 168, 72)):
        x = self.x * TILE
        y = self.y * TILE
        pygame.draw.rect(sc, pygame.Color(color), (x + 8, y + 8, TILE - 16, TILE - 16))

    def draw(self):
        x = self.x * TILE
        y = self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('black'), (x, y, TILE, TILE))

        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x + TILE, y), 1)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x + TILE, y), (x + TILE, y + TILE), 1)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y + TILE), (x + TILE, y + TILE), 1)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('darkorange'), (x, y), (x, y + TILE), 1)

    @staticmethod
    def find_index(x, y):
        return x + y * cols

    def check_cell(self, x, y):
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return self.grid_cells[Cell.find_index(x, y)]

    def check_neighbors(self, grid_cells):
        self.grid_cells = grid_cells
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False


class Maze:
    def __init__(self, show=False):
        self.grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.break_count = 1
        while self.break_count != len(self.grid_cells):
            self.current_cell.visited = True
            self.current_cell.draw_current_cell()
            next_cell = self.current_cell.check_neighbors(self.grid_cells)
            if next_cell:
                next_cell.visited = True
                self.stack.append(self.current_cell)
                self.remove_walls(self.current_cell, next_cell)
                self.current_cell = next_cell
                self.break_count += 1
            elif self.stack:
                self.current_cell = self.stack.pop()

            if show:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                [cell.draw() for cell in self.grid_cells]
                self.current_cell.draw_current_cell()
                clock.tick(5550)
                pygame.display.flip()

    def __call__(self, *args, **kwargs):
        return self.grid_cells

    def __getitem__(self, item):
        if 0 <= item < len(self.grid_cells):
            return self.grid_cells[item]
        else:
            raise IndexError('Ты перешел все границы')

    def __setitem__(self, key, value):
        if 0 <= key < len(self.grid_cells):
            self.grid_cells[key] = value
        elif key >= len(self.grid_cells):
            size = key - len(self.grid_cells)
            self.grid_cells.extend([0] * (size + 1))
            self.grid_cells[key] = value
        else:
            raise IndexError('Ты перешел все границы')

    def __delitem__(self, key):
        if 0 <= key < len(self.grid_cells):
            del self.grid_cells[key]
        else:
            raise IndexError('Ты перешел все границы')

    @staticmethod
    def remove_walls(current, follow):
        dx = current.x - follow.x
        dy = current.y - follow.y
        if dx == 1:
            current.walls['left'] = False
            follow.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            follow.walls['left'] = False
        if dy == 1:
            current.walls['top'] = False
            follow.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            follow.walls['top'] = False



