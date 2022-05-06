import pygame
from settings import *


class UI:
    def __init__(self, maze=None):
        self.screen = pygame.display.get_surface()
        self.maze = maze

        # Определение шрифтов
        self.f_sys = pygame.font.SysFont(FONT, 54)
        self.f_population_input = pygame.font.SysFont(FONT, 36)
        self.f_start_and_end = pygame.font.SysFont(FONT, round(TILE * 0.75))
        self.f_small = pygame.font.SysFont(FONT, 28)

    # Отрисовка лабиринта
    def show_maze(self):
        [cell.draw() for cell in self.maze.grid_cells]

    # Отрисовка точек конца и начала лабиринта
    def show_end_and_start_points(self, cell_finish):
        pygame.draw.rect(self.screen, (80, 100, 100), (1, 1 + TOP_PADDING, TILE - 1, TILE - 1))
        pygame.draw.rect(self.screen, (65, 80, 80), (cell_finish.x * TILE + 1, cell_finish.y * TILE + 1 + TOP_PADDING, TILE - 1, TILE - 1))
        text_start = self.f_start_and_end.render(f'S', True, ACTIVE_COLOR)
        text_finish = self.f_start_and_end.render(f'F', True, ACTIVE_COLOR)
        pos_finish = text_finish.get_rect(center=((cell_finish.x * TILE) + TILE / 2, (cell_finish.y * TILE) + TILE / 2 + TOP_PADDING))
        pos_start = text_start.get_rect(center=(TILE / 2, TILE / 2 + TOP_PADDING))
        self.screen.blit(text_start, pos_start)
        self.screen.blit(text_finish, pos_finish)

    def show_header(self):
        pygame.draw.rect(self.screen, HEADER_COLOR, (0, 0, WIDTH, TOP_PADDING))

    def show_header_buttons(self, first_btn_text=None, second_btn_text=None, third_btn_text=None):
        f_small = pygame.font.SysFont(FONT, 28)
        if first_btn_text:
            pygame.draw.rect(self.screen, STROKE_COLOR, (5, 5, WIDTH // 3 - 5, TOP_PADDING - 10))
            pygame.draw.rect(self.screen, HEADER_COLOR, (5 + 2, 5 + 2, WIDTH // 3 - 5 - 4, TOP_PADDING - 10 - 4))
            first_btn = f_small.render(first_btn_text, True, (180, 180, 180))
            pos_first_btn = first_btn.get_rect(center=(WIDTH // 3 / 2, TOP_PADDING / 2))
            self.screen.blit(first_btn, pos_first_btn)
        if second_btn_text:
            pygame.draw.rect(self.screen, STROKE_COLOR, (WIDTH // 3 + 5, 5, WIDTH // 3 - 5, TOP_PADDING - 10))
            pygame.draw.rect(self.screen, HEADER_COLOR,
                             (WIDTH // 3 + 5 + 2, 5 + 2, WIDTH // 3 - 5 - 4, TOP_PADDING - 10 - 4))
            second_btn = f_small.render(second_btn_text, True, (180, 180, 180))
            pos_second_btn = second_btn.get_rect(center=(WIDTH // 2, TOP_PADDING / 2))
            self.screen.blit(second_btn, pos_second_btn)
        if third_btn_text:
            pygame.draw.rect(self.screen, STROKE_COLOR, (WIDTH // 3 * 2 + 5, 5, WIDTH // 3 - 10, TOP_PADDING - 10))
            pygame.draw.rect(self.screen, HEADER_COLOR,
                             (WIDTH // 3 * 2 + 5 + 2, 5 + 2, WIDTH // 3 - 10 - 4, TOP_PADDING - 10 - 4))
            third_btn = f_small.render(third_btn_text, True, (180, 180, 180))
            pos_third_btn = third_btn.get_rect(center=(WIDTH * 8.3333 / 10, TOP_PADDING / 2))
            self.screen.blit(third_btn, pos_third_btn)