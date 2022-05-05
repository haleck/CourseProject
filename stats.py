from collections import Counter

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab

from genetic import Individual
from settings import *
import pygame
from ui import *


class StatSurface:
    def __init__(self, avg_values, leader: Individual):
        self.avg_values = avg_values
        self.sc = pygame.display.get_surface()
        self.length = len(leader.stack)
        self.turns = Counter(leader.stack).most_common(1)[0][1]

        self.UI = UI()

    def draw_stat(self):
        length_text = self.UI.f_sys.render(f'Length leader way: {self.length}', True, STROKE_COLOR, MAIN_BG)
        turns_text = self.UI.f_population_input.render(f'Number of turns: {self.turns}', True, STROKE_COLOR, MAIN_BG)
        pos1 = length_text.get_rect(center=(WIDTH / 2, HEIGHT // 1.5 + TOP_PADDING))
        pos2 = turns_text.get_rect(center=(WIDTH / 2, HEIGHT // 1.5 + 45 + TOP_PADDING))
        self.sc.blit(length_text, pos1)
        self.sc.blit(turns_text, pos2)
        pygame.display.flip()

    def draw_plot(self):
        plt.rcParams.update({
            "lines.linewidth": "1.8",
            "axes.prop_cycle": plt.cycler('color', ['white']),
            "text.color": STROKE_COLOR_HEX,
            "axes.facecolor": MAIN_BG_HEX,
            "axes.edgecolor": STROKE_COLOR_HEX,
            "axes.labelcolor": STROKE_COLOR_HEX,
            "axes.grid": "True",
            "grid.linestyle": "-.",
            "xtick.color": "white",
            "ytick.color": "white",
            "grid.color": STROKE_COLOR_HEX,
            "figure.facecolor": "black",
            "figure.edgecolor": "black",
        })

        fig = pylab.figure(figsize=[WIDTH // 150, HEIGHT // 150],  # Inches
                           dpi=100)  # 100 dots per inch, so the resulting buffer is 400x200 pixels
        fig.patch.set_alpha(0.1)  # make the surrounding of the plot 90% transparent to show what it does

        ax = fig.gca()
        ax.plot(self.avg_values, label="Fitness function value")
        ax.legend()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.buffer_rgba()

        pygame.init()

        size = canvas.get_width_height()
        surf = pygame.image.frombuffer(raw_data, size, "RGBA")

        self.sc.fill(MAIN_BG)
        self.sc.blit(surf, (200, TOP_PADDING + 30))
        pygame.display.flip()

    def draw_header(self):
        pygame.draw.rect(self.sc, HEADER_COLOR, (0, 0, WIDTH, TOP_PADDING))
        self.UI.show_header_buttons(first_btn_text='Back to maze', third_btn_text='Go to menu')

    def draw(self):
        self.draw_plot()
        stop = False
        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 5 <= event.pos[0] <= WIDTH // 3 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                        return 'back'
                    if WIDTH / 10 * 6.6666 + 5 <= event.pos[0] <= WIDTH - 5 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                        return 'exit'
            self.draw_header()
            self.draw_stat()
            pygame.display.update()
            pygame.time.Clock().tick(30)


