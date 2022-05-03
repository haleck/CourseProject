import pygame.pypm
from genetic import Population
from main import *


class MazeSolver:
    def __init__(self, MAX_POPULATION = DEFAULT_MAX_POPULATION, POPULATION_SIZE = DEFAULT_POPULATION_SIZE,
                 P_CROSSOVER = DEFAULT_P_CROSSOVER, P_MUTATION = DEFAULT_P_MUTATION):
        self.__MAX_POPULATION = MAX_POPULATION
        self.__POPULATION_SIZE = POPULATION_SIZE
        self.__P_CROSSOVER = P_CROSSOVER
        self.__P_MUTATION = P_MUTATION
        self.__population_number = 0
        self.__SHOW_EVOLUTION = SHOW_EVOLUTION
        self.__SHOW_MAZE_GENERATION = SHOW_MAZE_GENERATION
        self.__solution_drawn = False

    def set_max_population(self ,MAX_POPULATION):
        self.__MAX_POPULATION = MAX_POPULATION

    def set_population_size(self, POPULATION_SIZE):
        self.__POPULATION_SIZE = POPULATION_SIZE

    def set_p_crossover(self, P_CROSSOVER):
        self.__P_CROSSOVER = P_CROSSOVER

    def set_p_mutation(self, P_MUTATION):
        self.__P_MUTATION = P_MUTATION

    def set_evolution_show_mode(self, *value: tuple):
        self.__SHOW_EVOLUTION = True if value[1] == 2 else False

    def set_generation_show_mode(self, *value: tuple):
        self.__SHOW_MAZE_GENERATION = True if value[1] == 2 else False

    def start_passing(self):
        self.__MAX_ITERATION = self.__POPULATION_SIZE / TILE * 120
        self.__maze = Maze(show=self.__SHOW_MAZE_GENERATION)
        self.__population = Population(self.__maze)
        self.fitnessValues = [individual.individual_fitness for individual in self.__population.individuals]
        print('Value of MAX_POPULATION:', self.__MAX_POPULATION)
        print('Value of POPULATION_SIZE:', self.__POPULATION_SIZE)
        print('Value of P_CROSSOVER:', self.__P_CROSSOVER)
        print('Value of P_MUTATION:', self.__P_MUTATION)
        print('Value of MAX_ITERATION:', self.__MAX_ITERATION)

        # Определение шрифтов
        f_sys = pygame.font.SysFont(FONT, 54)
        f_population_input = pygame.font.SysFont(FONT, 36)
        f_small = pygame.font.SysFont(FONT, 28)
        f_start_and_end = pygame.font.SysFont(FONT, round(TILE * 0.75))

        # Отрисовка точек конца и начала лабиринта
        def show_end_and_start_points():
            pygame.draw.rect(sc, (80, 100, 100), (1, 1 + TOP_PADDING, TILE - 1, TILE - 1))
            pygame.draw.rect(sc, (65, 80, 80), (self.__maze[FINISH].x * TILE + 1, self.__maze[FINISH].y * TILE + 1 + TOP_PADDING, TILE - 1, TILE - 1))
            text_start = f_start_and_end.render(f'S', True, ACTIVE_COLOR)
            text_finish = f_start_and_end.render(f'F', True, ACTIVE_COLOR)
            pos_finish = text_finish.get_rect(center=((self.__maze[FINISH].x * TILE) + TILE / 2, (self.__maze[FINISH].y * TILE) + TILE / 2 + TOP_PADDING))
            pos_start = text_start.get_rect(center=(TILE / 2, TILE / 2 + TOP_PADDING))
            sc.blit(text_start, pos_start)
            sc.blit(text_finish, pos_finish)

        def show_processing(n_dots):
            text_processing = f_small.render(f'Processing' + '.' * n_dots, True, WHITE)
            pos_text_processing = text_processing.get_rect(center=(WIDTH / 2, TOP_PADDING / 2))
            sc.blit(text_processing, pos_text_processing)

        def show_header_buttons():
            pygame.draw.rect(sc, STROKE_COLOR, (5, 5, WIDTH // 3 - 5, TOP_PADDING - 10))
            pygame.draw.rect(sc, STROKE_COLOR, (WIDTH // 3 + 5, 5, WIDTH // 3 - 5, TOP_PADDING - 10))
            pygame.draw.rect(sc, STROKE_COLOR, (WIDTH // 3 * 2 + 5, 5, WIDTH // 3 - 10, TOP_PADDING - 10))
            pygame.draw.rect(sc, HEADER_COLOR, (5 + 2, 5 + 2, WIDTH // 3 - 5 - 4, TOP_PADDING - 10 - 4))
            pygame.draw.rect(sc, HEADER_COLOR, (WIDTH // 3 + 5 + 2, 5 + 2, WIDTH // 3 - 5 - 4, TOP_PADDING - 10 - 4))
            pygame.draw.rect(sc, HEADER_COLOR, (WIDTH // 3 * 2 + 5 + 2, 5 + 2, WIDTH // 3 - 10 - 4, TOP_PADDING - 10 - 4))
            btn_exit = f_small.render(f'Back to settings', True, (180, 180, 180))
            btn_replay = f_small.render(f'Replay', True, (180, 180, 180))
            btn_stats = f_small.render(f'Check stat', True, (180, 180, 180))
            pos_btn_exit = btn_exit.get_rect(center=(WIDTH // 3 / 2, TOP_PADDING / 2))
            pos_btn_replay = btn_replay.get_rect(center=(WIDTH // 2, TOP_PADDING / 2))
            pos_btn_stats = btn_stats.get_rect(center=(WIDTH * 8.3333 / 10, TOP_PADDING / 2))
            sc.blit(btn_exit, pos_btn_exit)
            sc.blit(btn_replay, pos_btn_replay)
            sc.blit(btn_stats, pos_btn_stats)

        def open_stat_window():
            stat_surface = pygame.Surface((WIDTH, HEIGHT + TOP_PADDING))
            stat_surface.fill(MAIN_BG)
            sc.blit(stat_surface, (0, 0))
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                pygame.time.delay(100)

        def iteration_loop():
            # Отрисовка процесса популяции при выключенной анимации
            def show_population_progress():
                sc_text = f_sys.render(f'Individual development', True, WHITE, MAIN_BG)
                population_text = f_population_input.render(
                    f'Population {self.__population_number + 1}/{self.__MAX_POPULATION}', True, WHITE, MAIN_BG)
                iteration_text = f_small.render(f'Step {iteration_counter + 1}/{round(self.__MAX_ITERATION)}',
                                                          True, WHITE, MAIN_BG)
                pos1 = sc_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30))
                pos2 = population_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 30))
                pos3 = iteration_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 80))
                sc.fill(MAIN_BG)
                sc.blit(sc_text, pos1)
                sc.blit(population_text, pos2)
                sc.blit(iteration_text, pos3)
                pygame.display.flip()

            iteration_counter = 0
            while iteration_counter < self.__MAX_ITERATION:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

                # Отрисовка элементов верхнего меню
                pygame.draw.rect(sc, HEADER_COLOR, (0, 0, WIDTH, TOP_PADDING))

                # Отрисовка положения каждой особи
                if self.__SHOW_EVOLUTION:
                    [cell.draw() for cell in self.__maze.grid_cells]
                else:
                    show_population_progress()

                # Определение следующего шага для каждой особи
                for ind in self.__population.individuals:
                    if ind.current_cell != self.__maze[FINISH]:
                        if ind.stack and len(ind.stack) > iteration_counter + 1:
                            ind.move_to(ind.stack[iteration_counter + 1], add=False)
                        else:
                            ind.move_to(ind.choose_next())
                        if self.__SHOW_EVOLUTION:
                            ind.current_cell.draw_current_cell()
                    elif ind.stack[-1] != self.__maze[FINISH]:
                        ind.stack.append(self.__maze[FINISH])
                if self.__SHOW_EVOLUTION:
                    show_end_and_start_points()
                    pygame.display.flip()
                iteration_counter += 1

        # Эволюционный процесс
        while self.__population_number < self.__MAX_POPULATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # Каждая особь проходит свой маршрут для обновления полей класса
            iteration_loop()

            # Турнирный отбор для новой популяции
            offspring = Population.sel_tournament(self.__population.individuals, len(self.__population.individuals))
            offspring = list(map(lambda ind1: Population.clone(self.__population, ind1), offspring))

            # Скрещивание индивидуумов популяции
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random() < self.__P_CROSSOVER:
                    Population.cx_two_points(child1, child2)

            # Мутация индивидуумов популяции
            for mutant in offspring:
                if random() < self.__P_MUTATION:
                    Population.mut(self.__population, mutant)

            # Обновление значений приспособленности
            fresh_fitness_values = list(map(Individual.fitness, offspring))
            for individual, fitnessValue in zip(offspring, fresh_fitness_values):
                individual.individual_fitness = fitnessValue

            self.__population.individuals[:] = offspring

            # Индивидуумы ставятся на начальную позицию
            for ind in self.__population.individuals:
                ind.route = 0
                ind.current_cell = self.__maze[0]
                ind.current_index = 0

            # Консольная информация
            print('----------------------------------------------------------------')
            print("Популяция", self.__population_number + 1)
            min_distance = min(self.__population.individuals, key=lambda indi: indi.individual_fitness).individual_fitness
            print(f'Минимальное значение функции приспособленности: {min_distance}')
            mean_distance = sum(fresh_fitness_values) / len(self.__population.individuals)
            print(f'Среднее значение функции приспособленности: {mean_distance}')

            self.__population_number += 1

        # Отбор лучшей особи
        leader = min(self.__population.individuals, key=lambda indi: indi.individual_fitness)

        # Удаление нулевых движений
        i = 0
        while i < len(leader.stack) - 1:
            if leader.stack[i] == leader.stack[i + 1]:
                leader.stack = leader.stack[:i] + leader.stack[i + 1:]
            else:
                i += 1

        # Отрисовка лучшего решения
        def draw_the_solution():
            sc.fill(MAIN_BG)
            not_drawn = True
            opened = True
            while opened:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 5 <= event.pos[0] <= WIDTH // 3 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                            MazeSolver.__init__(self, self.__MAX_POPULATION, self.__POPULATION_SIZE, self.__P_CROSSOVER, self.__P_MUTATION)
                            return
                        if WIDTH / 10 * 3.3333 + 5 <= event.pos[0] <= WIDTH / 10 * 6.6666 - 5 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                            self.__solution_drawn = True
                            opened = False
                            draw_the_solution()
                            return
                        if WIDTH / 10 * 6.6666 + 5 <= event.pos[0] <= WIDTH - 5 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                            open_stat_window()

                if not_drawn:
                    n_dots = 0
                    for indx in range(len(leader.stack) - 1):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                exit()

                        # Отрисовка элементов верхнего меню
                        pygame.draw.rect(sc, HEADER_COLOR, (0, 0, WIDTH, TOP_PADDING))
                        if indx % 20 == 0:
                            if n_dots == 3:
                                n_dots = 0
                            n_dots += 1
                        show_processing(n_dots)

                        # Отрисовка движения лучшей особи
                        [cell.draw() for cell in self.__maze.grid_cells]
                        if leader.stack[indx - 1]:
                            Individual.draw_the_way(leader.stack[indx - 1], leader.stack[indx], leader.stack[indx + 1])
                        leader.stack[indx].visited = False

                        # Отрисовка точек конца и начала лабиринта
                        show_end_and_start_points()

                        # Смена кадра
                        pygame.display.flip()
                        clock.tick(30)

                not_drawn = False

                [cell.draw() for cell in self.__maze.grid_cells]
                pygame.draw.rect(sc, HEADER_COLOR, (0, 0, WIDTH, TOP_PADDING))
                show_header_buttons()
                show_end_and_start_points()
                pygame.display.flip()

        if not self.__solution_drawn:
            draw_the_solution()
