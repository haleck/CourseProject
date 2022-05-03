# Animation settings
SHOW_EVOLUTION = False
SHOW_MAZE_GENERATION = False
TOP_PADDING = 50
MAIN_BG = (35, 36, 30)
STROKE_COLOR = (90, 89, 88)

# Settings of the screen
WIDTH, HEIGHT = 1200, 881
RES = WIDTH, HEIGHT + TOP_PADDING
TILE = 40
cols, rows = WIDTH // TILE, HEIGHT // TILE
FINISH = cols*rows-1

# Basic settings for genetic algorithm
DEFAULT_MAX_POPULATION = 30
DEFAULT_POPULATION_SIZE = 100
DEFAULT_P_CROSSOVER = 0.9
DEFAULT_P_MUTATION = 0.3
