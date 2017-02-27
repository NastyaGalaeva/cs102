from pygame.locals import *
import random
from pprint import pprint as pp
import pygame

#####################ИГРА БЕЗ СОБСТВЕННЫХ КЛАССОВ
class GameOfLife: # Создаем класс игры
    def __init__(self, width = 640, height = 480, cell_size = 1, speed = 50):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed


    def draw_grid(self):  # метод отрисовки таблицы
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (0, y), (self.width, y))


    def run(self): #запуск игры
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist) # Рисуем клетки, которые у нас находятся в clist
            self.update_cell_list(self.clist) # Обновляем
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self): # Метод генерации случайным способом клеток ( 1 - живая, 0 - мертвая)
        list = [[random.randint(0, 1)#Каждому i в каждой строке я присваиваю случайное значение 1 или 0
        for i in range(self.cell_width)]
        for i in range(self.cell_height)]
        return list


    def draw_cell_list(self, rects): # Метод отрисовки сетки с заполнением клеток цветом
        for i in range(len(rects)):
            for j in range(len(rects[i])):#Прохожусь по всем элементам(в каждой строке)
                if rects[i][j] == 0:#Если значение равно 0, то клетка будет белая
                    pygame.draw.rect(self.screen, pygame.Color('white'), (j*self.cell_size+1, i*self.cell_size+1, self.cell_size-1, self.cell_size-1))#координаты прямоугольника в формате (x, y, длина стороны a, длина стороны b)
                elif rects[i][j] == 1:#Иначе окрашиваю в зеленый
                    pygame.draw.rect(self.screen, pygame.Color('green'), (j*self.cell_size+1, i*self.cell_size+1, self.cell_size-1, self.cell_size-1))


    def get_neighbours(self, clist, x, y): # x, y – координаты. Находим соседей в clist для клетки по координатам (x, y)
        area = (-1, 0, 1) # Область, по индексам которой мы ищем соседей
        neighbours = [] # Объявляем пустой список соседей
        for i in area:
            for j in area:
                if (i | j) and (x+i >= 0) and (y+j >= 0): # Если i и j != 0(т.е не сама клетка) и нет выхода за границы списка (индекс не уходит в отрицательные числа)
                    try:
                        neighbours.append(clist[x+i][y+j]) # Добавляем соседа в список соседей
                    except IndexError:
                        pass
        return neighbours # Возвращаем список соседей

    def update_cell_list(self, cell_list): # Метод обновления таблицы с клетками
        new_cell_list = cell_list # Объявляем новый список, чтобы в нем поместить обновленные клетки
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if cell_list[i][j]: # Если клетка по координатам (i, j) живая, то:
                    if sum(self.get_neighbours(self.clist, i, j)) not in (2, 3): # Если кол-во соседей не 2 и не 3
                        new_cell_list[i][j] = 0 # То она становится мертвой
                    else:
                        new_cell_list[i][j] = 1 # Иначе она живая
                else: # Иначе (то есть ести клетка неживая)
                    if sum(self.get_neighbours(self.clist, i, j)) == 3: # Если кол-во соседей равно трем
                        new_cell_list[i][j] = 1 # Клетка становится живой
                    else:
                        new_cell_list[i][j] = 0  # Иначе остается мертвой

        self.clist = new_cell_list # Новый список ставится на место текущего


if __name__ == '__main__':
    game1 = GameOfLife(320, 240, 20)
    game1.run()