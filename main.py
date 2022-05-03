import pygame_menu
from genetic import *
from passing import *

if __name__ == '__main__':
    surface = pygame.display.set_mode(RES)
    MAIN_THEME = pygame_menu.themes.THEME_DARK.copy()
    MAX_POPULATION = POPULATION_SIZE = P_CROSSOVER = P_MUTATION = None
    executor = MazeSolver()

    menu = pygame_menu.Menu('Settings', WIDTH, HEIGHT+TOP_PADDING, theme=MAIN_THEME)

    menu.add.button('Start evolution!', executor.start_passing)
    menu.add.text_input('Number of populations: ',
                        input_type=pygame_menu.locals.INPUT_INT,
                        maxchar=3,
                        default=str(DEFAULT_MAX_POPULATION),
                        onchange=executor.set_max_population)
    menu.add.text_input('Population size: ',
                        input_type=pygame_menu.locals.INPUT_INT,
                        maxchar=4,
                        default=str(DEFAULT_POPULATION_SIZE),
                        onchange=executor.set_population_size)
    menu.add.text_input('Probability of crossover: 0.',
                        input_type=pygame_menu.locals.INPUT_FLOAT,
                        maxchar=1,
                        default=str(int(DEFAULT_P_CROSSOVER * 10)),
                        onchange=executor.set_p_crossover)
    menu.add.text_input('Probability of mutation: 0.',
                        input_type=pygame_menu.locals.INPUT_FLOAT,
                        maxchar=1, default=str(int(DEFAULT_P_MUTATION * 10)),
                        onchange=executor.set_p_mutation)
    menu.add.selector('Show evolution : ', [('OFF', 1), ('ON', 2)], onchange=executor.set_evolution_show_mode)
    menu.add.selector('Show maze generation : ', [('OFF', 1), ('ON', 2)], onchange=executor.set_generation_show_mode)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)
