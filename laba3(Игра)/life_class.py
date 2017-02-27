import pygame
from pygame.locals import *
import random
from pprint import pprint as pp

#############################ИГРА С СОЗДАННЫМИ КЛАССАМИ
class GameOfLife: #Создаем класс игры
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


    def draw_grid(self): #метод отрисовки таблицы
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (0, y), (self.width, y))


    def run(self):#запуск игры
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        cell_list = CellList(nrow=self.cell_height, ncol=self.cell_width)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(cell_list)#рисуем клетки, которые находятся в cell_list
            cell_list.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


    def draw_cell_list(self, cell_list):# Метод отрисовки сетки с заполнением клеток цветом
        green = pygame.Color('green')
        white = pygame.Color('white')
        for i in range(cell_list.nrow):
            for j in range(cell_list.ncol):#Прохожусь по всем элементам(для строки и строчки)
                x = (self.cell_size * (j)) + 1 #координаты прямоугольника в формате (x, y,  width - длина стороны a, длина стороны b)
                y = (self.cell_size * (i)) + 1
                width = self.cell_size - 1
                color = green if cell_list.clist[i][j].is_alive else white #Если клетка из Cell с параметром 'живая', то окрашиваю в зеленый, иначе она белая
                pygame.draw.rect(self.screen, color, (x, y, width, width))


class Cell(): #Класс клеток
    def __init__(self, is_alive):#Существует единственный параметр клеток - живая или нет
        self.is_alive = is_alive


class CellList(GameOfLife):#генерирую числа, нахожу соседей, узнаю живая она или мертвая
    def __init__(self, **kwargs):#** указывает на то, что могут быть несколько ключей
        if'nrow' in kwargs and 'ncol' in kwargs:#Если указаны эти ключи в функции ran, то создаю список = функции generate
            self.nrow = kwargs['nrow']
            self.ncol = kwargs['ncol']
            self.clist = self._generate(self.ncol, self.nrow)


    def _generate(self, ncol, nrow):# Метод генерации случайным способом клеток ( 1 - живая, 0 - мертвая)
        list = [[Cell(random.randint(0, 1))#Каждому i в каждой строке я присваиваю случайное значение 1 или 0 - список находится в классе Cell
        for i in range(ncol)]
        for i in range(nrow)]
        return list


    def get_neighbours(self, x, y):#x, y – координаты. Находим соседей в clist для клетки по координатам (x, y)
        area = (-1, 0, 1)# Область, по индексам которой мы ищем соседей
        neighbours = []# Объявляем пустой список соседей
        for i in area:
            for j in area:
                if (i | j) and (x+i >= 0) and (y+j >= 0):# Если i и j != 0(т.е не сама клетка) и нет выхода за границы списка (индекс не уходит в отрицательные числа)
                    try:
                        neighbours.append(self.clist[x+i][y+j].is_alive)# Присваиваю соседу параметр 'живой' в Cell
                    except IndexError:
                        pass
        return neighbours


    def update(self):#метод обновления клеток
        new_cell_list = self.clist#объявляю новый список, чтобы в нем поместить обновленные клетки
        for i in range(self.nrow):
            for j in range(self.ncol):
                if self.clist[i][j]:# Если клетка по координатам (i, j) живая, то:
                    if sum(self.get_neighbours(i, j)) not in (2, 3):# Если кол-во соседей не 2 и не 3
                        new_cell_list[i][j] = Cell(0)# То она становится мертвой в Cell
                    else:
                        new_cell_list[i][j] = Cell(1)# Иначе она живая в Cell
                else:# Иначе (то есть ести клетка неживая)
                    if sum(self.get_neighbours(i, j)) == 3:# Если кол-во соседей равно трем
                        new_cell_list[i][j] = Cell(1)#клетка становится живой в Cell
                    else:
                        new_cell_list[i][j] = Cell(0)#иначе остается мертвой в Cell

        self.clist = new_cell_list # Новый список ставится на место текущего



if __name__ == '__main__':
    game1 = GameOfLife(320, 240, 20)
    game1.run()