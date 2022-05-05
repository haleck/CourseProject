import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab
from settings import *
import pygame
from ui import *


class StatSurface:
    def __init__(self, avg_values):
        self.avg_values = avg_values
        self.sc = pygame.display.get_surface()

        self.UI = UI()

    def draw_stat(self):
        pass

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

        fig = pylab.figure(figsize=[WIDTH // 200, HEIGHT // 200],  # Inches
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
        self.sc.blit(surf, (100, TOP_PADDING + 30))
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
            self.draw_header()
            pygame.display.update()
            pygame.time.Clock().tick(30)


