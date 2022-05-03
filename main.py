import pygame_menu
from genetic import *

if __name__ == '__main__':
    surface = pygame.display.set_mode(RES)
    MAIN_THEME = pygame_menu.themes.THEME_DARK.copy()

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


    menu = pygame_menu.Menu('Settings', WIDTH, HEIGHT+TOP_PADDING, theme=MAIN_THEME)

    menu.add.text_input('Number of populations: ',
                        input_type=pygame_menu.locals.INPUT_INT,
                        maxchar=3,
                        default=str(MAX_POPULATION),
                        onchange=save_number_population)

    menu.add.text_input('Population size: ',
                        input_type=pygame_menu.locals.INPUT_INT,
                        maxchar=4,
                        default=str(POPULATION_SIZE),
                        onchange=save_population_size)

    menu.add.text_input('Probability of crossover: 0.',
                        input_type=pygame_menu.locals.INPUT_FLOAT,
                        maxchar=1,
                        default=str(int(P_CROSSOVER * 10)),
                        onchange=save_p_crossover)

    menu.add.text_input('Probability of mutation: 0.',
                        input_type=pygame_menu.locals.INPUT_FLOAT,
                        maxchar=1, default=str(int(P_MUTATION * 10)),
                        onchange=save_p_mutation)

    menu.add.selector('Show evolution : ', [('OFF', 1), ('ON', 2)], onchange=save_evolution_show_mode)
    menu.add.selector('Show maze generation : ', [('OFF', 1), ('ON', 2)], onchange=save_generation_show_mode)


    def start_the_game():
        MAX_ITERATION = POPULATION_SIZE / TILE * 120
        print('Value of MAX_POPULATION:', MAX_POPULATION)
        print('Value of POPULATION_SIZE:', POPULATION_SIZE)
        print('Value of P_CROSSOVER:', P_CROSSOVER)
        print('Value of P_MUTATION:', P_MUTATION)
        print('Value of MAX_ITERATION:', MAX_ITERATION)
        maze = Maze(show=SHOW_MAZE_GENERATION)
        population = Population(maze)
        fitnessValues = [individual.individual_fitness for individual in population.individuals]
        population_number = 0

        # Определение шрифтов
        f_sys = pygame.font.SysFont('times_new_roman', 54)
        f_population_input = pygame.font.SysFont('times_new_roman', 36)
        f_iteration_input = pygame.font.SysFont('times_new_roman', 28)
        f_start_and_end = pygame.font.SysFont('times_new_roman', round(TILE * 0.75))

        # Отрисовка процесса популяции при выключенной анимации
        def show_population_progress():
            sc_text = f_sys.render(f'Individual development', True, (255, 255, 255), MAIN_BG)
            population_text = f_population_input.render(f'Population {population_number + 1}/{MAX_POPULATION}', True,(255, 255, 255), MAIN_BG)
            iteration_text = f_iteration_input.render(f'Step {iteration_counter + 1}/{round(MAX_ITERATION)}', True,(255, 255, 255), MAIN_BG)
            pos1 = sc_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30))
            pos2 = population_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 30))
            pos3 = iteration_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 80))
            sc.fill(MAIN_BG)
            sc.blit(sc_text, pos1)
            sc.blit(population_text, pos2)
            sc.blit(iteration_text, pos3)
            pygame.display.flip()

        # Отрисовка точек конца и начала лабиринта
        def show_end_and_start_points():
            pygame.draw.rect(sc, (80, 100, 100),(maze[0].x + 1, maze[0].y + 1 + TOP_PADDING, maze[0].x + TILE - 1, maze[0].y + TILE - 1))
            pygame.draw.rect(sc, (65, 80, 80), (maze[FINISH].x * TILE + 1, maze[FINISH].y * TILE + 1 + TOP_PADDING, TILE, TILE))
            text_start = f_start_and_end.render(f'S', True, (0, 196, 34))
            text_finish = f_start_and_end.render(f'F', True, (0, 196, 34))
            pos_finish = text_finish.get_rect(center=((maze[FINISH].x * TILE) + TILE / 2, (maze[FINISH].y * TILE) + TILE / 2 + TOP_PADDING))
            pos_start = text_start.get_rect(center=((maze[0].x * TILE) + TILE / 2, (maze[0].y * TILE) + TILE / 2 + TOP_PADDING))
            sc.blit(text_start, pos_start)
            sc.blit(text_finish, pos_finish)

        # Эволюционный процесс
        while population_number < MAX_POPULATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            iteration_counter = 0
            while iteration_counter < MAX_ITERATION:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

                # Отрисовка положения каждой особи
                if SHOW_EVOLUTION:
                    [cell.draw() for cell in maze.grid_cells]
                else:
                    show_population_progress()

                # Определение следующего шага для каждой особи
                for ind in population.individuals:
                    if ind.current_cell != maze[FINISH]:
                        if ind.stack and len(ind.stack) > iteration_counter + 1:
                            ind.move_to(ind.stack[iteration_counter + 1], add=False)
                        else:
                            ind.move_to(ind.choose_next())
                        if SHOW_EVOLUTION:
                            ind.current_cell.draw_current_cell()
                    elif ind.stack[-1] != maze[FINISH]:
                        ind.stack.append(maze[FINISH])

                iteration_counter += 1
                if SHOW_EVOLUTION:
                    show_end_and_start_points()
                    pygame.display.flip()

            print('----------------------------------------------------------------')
            print("Популяция", population_number + 1)

            # Турнирный отбор для новой популяции
            offspring = Population.sel_tournament(population.individuals, len(population.individuals))
            offspring = list(map(lambda ind1: Population.clone(population, ind1), offspring))

            # Скрещивание индивидуумов популяции
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random() < P_CROSSOVER:
                    Population.cx_two_points(child1, child2)

            # Мутация индивидуумов популяции
            for mutant in offspring:
                if random() < P_MUTATION:
                    Population.mut(population, mutant)

            # Обновление значений приспособленности
            fresh_fitness_values = list(map(Individual.fitness, offspring))
            for individual, fitnessValue in zip(offspring, fresh_fitness_values):
                individual.individual_fitness = fitnessValue

            population.individuals[:] = offspring

            # Индивидуумы ставятся на начальную позицию
            for ind in population.individuals:
                ind.route = 0
                ind.current_cell = maze[0]
                ind.current_index = 0

            min_distance = min(population.individuals, key=lambda indi: indi.individual_fitness).individual_fitness
            print(f'Минимальное значение функции приспособленности: {min_distance}')
            mean_distance = sum(fresh_fitness_values) / len(population.individuals)
            print(f'Среднее значение функции приспособленности: {mean_distance}')

            population_number += 1

        # Отбор лучшей особи
        leader = min(population.individuals, key=lambda indi: indi.individual_fitness)

        # Удаление нулевых движений
        i = 0
        while i < len(leader.stack) - 1:
            if leader.stack[i] == leader.stack[i + 1]:
                leader.stack = leader.stack[:i] + leader.stack[i + 1:]
            else:
                i += 1

        # Отрисовка лучшего решения
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            for indx in range(len(leader.stack) - 1):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

                # Отрисовка элементов верхнего меню
                pygame.draw.rect(sc, (47, 48, 51), (0, 0, WIDTH, TOP_PADDING))

                # Отрисовка движения лучшей особи
                [cell.draw() for cell in maze.grid_cells]
                if leader.stack[indx - 1]:
                    Individual.draw_the_way(leader.stack[indx - 1], leader.stack[indx], leader.stack[indx + 1])
                leader.stack[indx].visited = False

                # Отрисовка точек конца и начала лабиринта
                show_end_and_start_points()

                # Смена кадра
                pygame.display.flip()
                clock.tick(30)

            [cell.draw() for cell in maze]
            pygame.display.flip()


    menu.add.button('Start evolution!', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)
