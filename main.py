import pygame_menu
from genetic import *
from passing import *

if __name__ == '__main__':
    surface = pygame.display.set_mode(RES)
    MAIN_THEME = pygame_menu.themes.THEME_DARK.copy()
    MAX_POPULATION = POPULATION_SIZE = P_CROSSOVER = P_MUTATION = None

    def save_number_population(value):
        print('Change in save_number_population')
        global MAX_POPULATION
        MAX_POPULATION = value

    def save_population_size(value):
        print('Change in save_population_size')
        global POPULATION_SIZE
        POPULATION_SIZE = value

    def save_p_crossover(value):
        print('Change in save_p_crossover')
        global P_CROSSOVER
        P_CROSSOVER = value*0.1

    def save_p_mutation(value):
        print('Change in save_p_mutation')
        global P_MUTATION
        P_MUTATION = value*0.1

    def save_evolution_show_mode(*value: tuple):
        print('Change in save_evolution_show_mode')
        global SHOW_EVOLUTION
        SHOW_EVOLUTION = True if value[1] == 2 else False

    def save_generation_show_mode(*value: tuple):
        print('Change in save_generation_show_mode')
        global SHOW_MAZE_GENERATION
        SHOW_MAZE_GENERATION = True if value[1] == 2 else False

    def update_params():
        start_passing(MAX_POPULATION, POPULATION_SIZE, P_CROSSOVER, P_MUTATION)


    menu = pygame_menu.Menu('Settings', WIDTH, HEIGHT+TOP_PADDING, theme=MAIN_THEME)

    menu.add.text_input('Number of populations: ',
                        input_type=pygame_menu.locals.INPUT_INT,
                        maxchar=3,
                        default=str(DEFAULT_MAX_POPULATION),
                        onchange=save_number_population)

    menu.add.text_input('Population size: ',
                        input_type=pygame_menu.locals.INPUT_INT,
                        maxchar=4,
                        default=str(DEFAULT_POPULATION_SIZE),
                        onchange=save_population_size)

    menu.add.text_input('Probability of crossover: 0.',
                        input_type=pygame_menu.locals.INPUT_FLOAT,
                        maxchar=1,
                        default=str(int(DEFAULT_P_CROSSOVER * 10)),
                        onchange=save_p_crossover)

    menu.add.text_input('Probability of mutation: 0.',
                        input_type=pygame_menu.locals.INPUT_FLOAT,
                        maxchar=1, default=str(int(DEFAULT_P_MUTATION * 10)),
                        onchange=save_p_mutation)

    menu.add.selector('Show evolution : ', [('OFF', 1), ('ON', 2)], onchange=save_evolution_show_mode)
    menu.add.selector('Show maze generation : ', [('OFF', 1), ('ON', 2)], onchange=save_generation_show_mode)

    menu.add.button('Start evolution!', update_params)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)
