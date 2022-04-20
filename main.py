from genetic import *

if __name__ == '__main__':
    maze = Maze(show=False)
    population = Population(maze)
    fitnessValues = [individual.individual_fitness for individual in population.individuals]
    population_number = 0

    # Определение шрифтов
    f_sys = pygame.font.SysFont('times_new_roman', 54)
    f_population_input = pygame.font.SysFont('times_new_roman', 36)
    f_start_and_end = pygame.font.SysFont('times_new_roman', round(TILE*0.75))

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
                sc_text = f_sys.render(f'Происходит эволюция', True, (255, 255, 255), (0, 0, 0))
                population_text = f_population_input.render(f'Популяция {population_number+1}/{MAX_POPULATION}', True,
                                       (255, 255, 255), (0, 0, 0))
                pos1 = sc_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30))
                pos2 = population_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 30))
                sc.fill((0, 0, 0))
                sc.blit(sc_text, pos1)
                sc.blit(population_text, pos2)
                pygame.display.flip()

            # Определение следующего шага для каждой особи
            for ind in population.individuals:
                if ind.current_cell != maze[FINISH]:
                    if ind.stack and len(ind.stack) > iteration_counter + 1:
                        ind.move_to(ind.stack[iteration_counter + 1], add=False)
                    else:
                        ind.move_to(ind.choose_next())
                    if SHOW_EVOLUTION:
                        ind.current_cell.draw_current_cell()
                else:
                    ind.stack.append(maze[FINISH])

            iteration_counter += 1
            if SHOW_EVOLUTION:
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

        print('10 случайных значений длины пути из популяции:')
        print([population.individuals[i].route for i in range(10)])

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
    while i < len(leader.stack)-1:
        if leader.stack[i] == leader.stack[i+1]:
            leader.stack = leader.stack[:i] + leader.stack[i+1:]
        else:
            i += 1

    # Отрисовка лучшего решения
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        for indx in range(len(leader.stack)-1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            # Отрисовка движения лучшей особи
            [cell.draw() for cell in maze.grid_cells]
            if leader.stack[indx-1]:
                Individual.draw_the_way(leader.stack[indx-1], leader.stack[indx], leader.stack[indx+1])
            leader.stack[indx].visited = False

            # Отрисовка точек конца и начала лабиринта
            pygame.draw.rect(sc, (80, 100, 100), (maze[0].x+1, maze[0].y+1, maze[0].x+TILE-1, maze[0].y+TILE-1))
            pygame.draw.rect(sc, (65, 80, 80), (maze[FINISH].x * TILE + 1, maze[FINISH].y * TILE + 1, TILE, TILE))
            text_start = f_start_and_end.render(f'S', True, (0, 196, 34))
            text_finish = f_start_and_end.render(f'F', True, (0, 196, 34))
            pos_finish = text_finish.get_rect(center=((maze[FINISH].x * TILE) + TILE / 2, (maze[FINISH].y * TILE) + TILE / 2))
            pos_start = text_start.get_rect(center=((maze[0].x * TILE) + TILE / 2, (maze[0].y * TILE) + TILE / 2))
            sc.blit(text_start, pos_start)
            sc.blit(text_finish, pos_finish)

            # Смена кадра
            pygame.display.flip()
            clock.tick(30)

        [cell.draw() for cell in maze]
        pygame.display.flip()
