from pstats import Stats
import pygame.pypm
from genetic import Population
from main import *
from stats import *
from ui import *


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
        self.avg_values = []
        self.__MAX_ITERATION = 1 / TILE ** 0.90 * 15000
        self.__maze = None
        self.UI = UI()
        self.__population = None
        self.fitnessValues = None

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
        return

    # Выполнение шагов всеми индивидуумами
    def iteration_loop(self):
        iteration_counter = 0
        while iteration_counter < self.__MAX_ITERATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.UI.show_header()

            # Отрисовка положения каждой особи
            self.UI.show_maze() if self.__SHOW_EVOLUTION else self.show_population_progress(iteration_counter)

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
                self.UI.show_end_and_start_points(self.__maze[FINISH])
                pygame.display.flip()
            iteration_counter += 1

    # По популяции класса отбирает лучшую особь
    def define_leader(self):
        leader = min(self.__population.individuals, key=lambda indi: indi.individual_fitness)

        # Удаление нулевых движений
        i = 0
        while i < len(leader.stack) - 1:
            if leader.stack[i] == leader.stack[i + 1]:
                leader.stack = leader.stack[:i] + leader.stack[i + 1:]
            else:
                i += 1

        return leader

    # Выводит информацию о настройках генетического алгоритма в косноль
    def print_genetic_info(self):
        print('Value of MAX_POPULATION:', self.__MAX_POPULATION)
        print('Value of POPULATION_SIZE:', self.__POPULATION_SIZE)
        print('Value of P_CROSSOVER:', self.__P_CROSSOVER)
        print('Value of P_MUTATION:', self.__P_MUTATION)
        print('Value of MAX_ITERATION:', self.__MAX_ITERATION)

    # Выводит информацию об изменении популяции в консоль
    def print_console_info(self, fresh_fitness_values):
        print('----------------------------------------------------------------')
        print("Популяция", self.__population_number + 1)
        min_distance = min(self.__population.individuals, key=lambda indi: indi.individual_fitness).individual_fitness
        print(f'Минимальное значение функции приспособленности: {min_distance}')
        mean_distance = sum(fresh_fitness_values) / len(self.__population.individuals)
        self.avg_values.append(mean_distance)
        print(f'Среднее значение функции приспособленности: {mean_distance}')

    # Анимация процесса загрузки
    def show_processing(self, n_dots=0):
        text_processing = self.UI.f_small.render(f'Processing' + '.' * n_dots, True, WHITE)
        pos_text_processing = text_processing.get_rect(center=(WIDTH / 2, TOP_PADDING / 2))
        sc.blit(text_processing, pos_text_processing)

    # Выводит на экран стадию эволюции
    def show_population_progress(self, iteration_counter):
        sc_text = self.UI.f_sys.render(f'Individual development', True, WHITE, MAIN_BG)
        population_text = self.UI.f_population_input.render(
            f'Population {self.__population_number + 1}/{self.__MAX_POPULATION}', True, WHITE, MAIN_BG)
        iteration_text = self.UI.f_small.render(f'Step {iteration_counter + 1}/{round(self.__MAX_ITERATION)}', True,
                                                WHITE, MAIN_BG)
        pos1 = sc_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30))
        pos2 = population_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 30))
        pos3 = iteration_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 80))
        sc.fill(MAIN_BG)
        sc.blit(sc_text, pos1)
        sc.blit(population_text, pos2)
        sc.blit(iteration_text, pos3)
        pygame.display.flip()

    # Отрисовка лучшего решения
    def show_the_solution(self):

        leader = self.define_leader()

        sc.fill(MAIN_BG)
        not_drawn = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 5 <= event.pos[0] <= WIDTH // 3 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                        MazeSolver.__init__(self, self.__MAX_POPULATION, self.__POPULATION_SIZE, self.__P_CROSSOVER, self.__P_MUTATION)
                        sc.fill(MAIN_BG)
                        return
                    if WIDTH / 10 * 3.3333 + 5 <= event.pos[0] <= WIDTH / 10 * 6.6666 - 5 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                        self.__solution_drawn = True
                        self.show_the_solution()
                        sc.fill(MAIN_BG)
                        return
                    if WIDTH / 10 * 6.6666 + 5 <= event.pos[0] <= WIDTH - 5 and 5 <= event.pos[1] <= TOP_PADDING - 10:
                        # Открытие окна статистики прохождения лабаринта
                        stats = StatSurface(self.avg_values, leader)
                        callback = stats.show()
                        if callback == 'exit':
                            MazeSolver.__init__(self, self.__MAX_POPULATION, self.__POPULATION_SIZE, self.__P_CROSSOVER, self.__P_MUTATION)
                            sc.fill(MAIN_BG)
                            return
                        if callback == 'back':
                            self.__solution_drawn = True
                            self.show_the_solution()
                            sc.fill(MAIN_BG)
                            return

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
                    self.show_processing(n_dots)

                    # Отрисовка движения лучшей особи
                    self.UI.show_maze()
                    if leader.stack[indx - 1]:
                        Individual.draw_the_way(leader.stack[indx - 1], leader.stack[indx], leader.stack[indx + 1])
                    leader.stack[indx].visited = False

                    # Отрисовка точек конца и начала лабиринта
                    self.UI.show_end_and_start_points(self.__maze[FINISH])

                    # Смена кадра
                    pygame.display.flip()
                    pygame.time.Clock().tick(30)

            not_drawn = False
            self.UI.show_maze()
            self.UI.show_header()
            self.UI.show_header_buttons(first_btn_text='Back to settings', second_btn_text='Replay', third_btn_text='Check stat')
            self.UI.show_end_and_start_points(self.__maze[FINISH])
            pygame.display.flip()

    # Главная функция выполения алгоритма
    def start_passing(self):
        self.__maze = Maze(show=self.__SHOW_MAZE_GENERATION)
        self.UI = UI(self.__maze)
        self.__population = Population(self.__maze)
        self.fitnessValues = [individual.individual_fitness for individual in self.__population.individuals]

        self.print_genetic_info()

        # Эволюционный процесс
        while self.__population_number < self.__MAX_POPULATION:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # Каждая особь проходит лабиринт
            self.iteration_loop()

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

            # Удаление вспомогательного массива
            self.__population.individuals[:] = offspring

            # Индивидуумы ставятся на начальную позицию
            for ind in self.__population.individuals:
                ind.route = 0
                ind.current_cell = self.__maze[0]
                ind.current_index = 0

            # Выводятся результаты эволюции для поколения
            self.print_console_info(fresh_fitness_values)

            self.__population_number += 1

        # Выводится прохождение лабаринта лучшей особи
        if not self.__solution_drawn:
            self.show_the_solution()
