# Settings of the screen
RES = WIDTH, HEIGHT = 1200, 860
TILE = 30
cols, rows = WIDTH // TILE, HEIGHT // TILE
FINISH = cols*rows-1

# Basic settings for genetic algorithm
MAX_POPULATION = 1
POPULATION_SIZE = 50
MAX_ITERATION = POPULATION_SIZE/TILE*100
P_CROSSOVER = 0.9
P_MUTATION = 0.3

# Animation settings
SHOW_EVOLUTION = False
