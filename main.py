import pygame
import random
import copy
from PIL import Image
import sqlite3


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 40
        self.Pasha = 0
        self.display = pygame.display.set_mode((800,900))
        self.fon = Image.open('tetris.jpg')
        new_image = self.fon.resize((800, 900))
        new_image.save('tetris.jpg')
        self.fon = pygame.image.load('tetris.jpg')
        screen.blit(self.fon, (0, 0))


    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255),
                                 [self.top + i * self.cell_size, self.left + j * self.cell_size, self.cell_size,
                                  self.cell_size], 1)

    def state(self, screen, field):
        screen.fill((0, 0, 0))
        screen.blit(board.fon, (0, 0))
        self.render(screen)
        for i in range(self.width):
            for j in range(self.height):
                if field[j][i] == 1:
                    pygame.draw.rect(screen, (28, 98, 98),
                                     [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                      board.cell_size, board.cell_size])


class Shape:
    def __init__(self):
        self.stop = False
        self.shapes = ['square', 'stick', 'steps', 'zigzag_r', 'zigzag_l', 'turn_r', 'turn_l']
        self.shape_w = {'square': [[[4, 0], [4, 1], [5, 0], [5, 1]], (255, 255, 0)],
                        'stick': [[[6, 0], [5, 0], [4, 0], [3, 0]], (117, 187, 253)],
                        'steps': [[[5, 0], [4, 1], [5, 1], [6, 1]], (148, 0, 211)],
                        'zigzag_r': [[[3, 1], [4, 1], [4, 0], [5, 0]], (255, 0, 0)],
                        'zigzag_l': [[[4, 0], [5, 0], [5, 1], [6, 1]], (0, 255, 0)],
                        'turn_r': [[[3, 0], [3, 1], [4, 1], [5, 1]], (255, 192, 203)],
                        'turn_l': [[[5, 0], [3, 1], [4, 1], [5, 1]], (255, 91, 0)]

                        }
        self.shape_w1 = {'square': [[[4, 0], [4, 1], [5, 0], [5, 1]], (255, 255, 0)],
                         'stick': [[[6, 0], [5, 0], [4, 0], [3, 0]], (117, 187, 253)],
                         'steps': [[[5, 0], [4, 1], [5, 1], [6, 1]], (148, 0, 211)],
                         'zigzag_r': [[[3, 1], [4, 1], [4, 0], [5, 0]],  (255, 0, 0)],
                         'zigzag_l': [[[4, 0], [5, 0], [5, 1], [6, 1]], (0, 255, 0)],
                         'turn_r': [[[3, 0], [3, 1], [4, 1], [5, 1]], (255, 192, 203)],
                         'turn_l': [[[5, 0], [3, 1], [4, 1], [5, 1]], (255, 91, 0)]

                         }
        self.field = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.record = 0
        self.new_record = 0
        self.conn = sqlite3.connect("main_db.db")
        self.cursor = self.conn.cursor()
        self.max_record = self.cursor.execute("""SELECT num FROM records""").fetchall()
        print(self.max_record[0][0])

    def choose(self):
        n = random.randint(0, len(self.shapes) - 1)

        self.to_print = self.shapes[n]
        self.coord = self.shape_w[self.to_print][0]
        self.color = self.shape_w[self.to_print][1]
        self.step = 0
        self.bottom = False

    def draw_s(self, screen):
        for (i, j) in self.coord:
            pygame.draw.rect(screen, self.color,
                             [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                              board.cell_size, board.cell_size])

    def m_right(self, screen):
        k = 0

        board.state(screen, self.field)
        is_True = True
        for i in self.coord:
            m, n = i
            if m != 9:
                if self.field[n][m + 1] == 1:
                    is_True = False
            else:
                is_True = False
        if is_True:
            for i in self.coord:
                if i[0] != 9:
                    i[0] += 1
        for (i, j) in self.coord:
            if i <= 9:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])

    def m_left(self, screen):
        board.state(screen, self.field)
        is_True = True
        for i in self.coord:
            m, n = i
            if m != 0:
                if self.field[n][m - 1] == 1:
                    is_True = False
            else:
                is_True = False
        for i in self.coord:
            if i[0] == 0:
                is_True = False
        if is_True:
            for i in self.coord:
                if i[0] != 0:
                    i[0] -= 1
        for (i, j) in self.coord:
            pygame.draw.rect(screen, self.color,
                             [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                              board.cell_size, board.cell_size])

    def m_down(self, screen):
        board.state(screen, self.field)
        self.stop = True
        for i in self.coord:
            m, n = i
            if n != 19:
                if self.field[n + 1][m] == 1:
                    self.stop = False
            else:
                self.stop = False
        if self.stop:
            for i in self.coord:
                if i[1] != 19:
                    i[1] += 1
                # for j in self.field:
                #     if i == j:
                #         is_True = False

        for (i, j) in self.coord:
            pygame.draw.rect(screen, self.color,
                             [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                              board.cell_size, board.cell_size])
        if not self.stop:
            for (i, j) in self.coord:
                self.field[j][i] = 1
            self.choose()
            self.draw_s(screen)
            self.shape_w = copy.deepcopy(self.shape_w1)
            self.bottom = True

    def rotate(self, screen):
        board.state(screen, self.field)

        if self.to_print == 'stick':
            [[a, b], [c, d], [e, f], [g, h]] = self.coord
            if b != 19 and c != 9 and d > 1 and c > 1:
                if b == d:
                    k = 1
                else:
                    k = -1
                a -= 1 * k
                b -= 2 * k
                e += 1 * k
                f -= 1 * k
                g += 2 * k
                h += 1 * k
                if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                    self.coord = [[a, b], [c, d], [e, f], [g, h]]

            for (i, j) in self.coord:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])

        elif self.to_print == 'steps':
            [[a, b], [c, d], [e, f], [g, h]] = self.coord
            if e < 9 and a < 9 and e > 0 and f > 1 and f < 18:
                if self.step == 0:
                    c += 1
                    d += 1
                    self.step = (self.step + 1) % 4
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif self.step == 1:
                    b += 2
                    c -= 1
                    d -= 1
                    self.step = (self.step + 1) % 4
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif self.step == 2:
                    b -= 2
                    g -= 1
                    h += 1
                    self.step = (self.step + 1) % 4
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif self.step == 3:
                    g += 1
                    h -= 1
                    self.step = (self.step + 1) % 4
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]


            for (i, j) in self.coord:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])

        elif self.to_print == 'turn_r':
            [[a, b], [c, d], [e, f], [g, h]] = self.coord
            if e < 8 and f < 18 and a < 9 and b > 0:
                if a == c and f == h:
                    b -= 1
                    e -= 1
                    f -= 1
                    g -= 1
                    h -= 2
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif a == e and a != g:
                    a += 1
                    b += 1
                    c += 2
                    g += 1
                    h += 1
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif b == f and b == h:
                    b += 1
                    c -= 1
                    d -= 1
                    f += 1
                    g -= 1
                    h -= 1
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif c == g and c != h:
                    a -= 1
                    b -= 1
                    c -= 1
                    d += 1
                    e += 1
                    g += 1
                    h += 2
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

            for (i, j) in self.coord:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])



        elif self.to_print == 'turn_l':
            [[a, b], [c, d], [e, f], [g, h]] = self.coord
            if e < 9 and a < 9 and e > 0 and f > 1 and f < 18 and g < 9:

                if self.step == 0:
                    a -= 1
                    c += 1
                    d -= 2
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif self.step == 1:
                    b += 2
                    c += 2
                    d += 2
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif self.step == 2:
                    a += 1
                    b -= 1
                    c -= 1
                    d -= 1
                    f -= 2
                    h -= 2
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif self.step == 3:
                    b -= 1
                    c -= 2
                    d += 1
                    f += 2
                    h += 2
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                self.step = (self.step + 1) % 4

            for (i, j) in self.coord:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])


        elif self.to_print == 'zigzag_r':
            [[a, b], [c, d], [e, f], [g, h]] = self.coord
            print(self.coord)
            if e < 9:

                if b == d and d != f:
                    a += 2
                    b += 1
                    h += 1
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif d == h and b != f:
                    a -= 2
                    b -= 1
                    h -= 1
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

            print(self.coord)
            for (i, j) in self.coord:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])

        elif self.to_print == 'zigzag_l':
            [[a, b], [c, d], [e, f], [g, h]] = self.coord
            if e < 9:
                if b == d and a != g:
                    b += 1
                    g -= 2
                    h += 1
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]

                elif c == e and b == f:
                    b -= 1
                    g += 2
                    h -= 1
                    if self.field[b][a] == self.field[d][c] == self.field[f][e] == self.field[h][g] == 0:
                        self.coord = [[a, b], [c, d], [e, f], [g, h]]


            for (i, j) in self.coord:
                pygame.draw.rect(screen, self.color,
                                 [board.top + 1 + i * board.cell_size, board.left + 1 + j * board.cell_size,
                                  board.cell_size, board.cell_size])
            else:
                pass


pygame.init()
size = width, height = 400, 400
screen = pygame.display.set_mode(size)
surface = pygame.display.set_mode()
board = Board(10, 20)
running = True
shape = Shape()
shape.choose()
shape.draw_s(screen)
clock = pygame.time.Clock()
fps = 5
fps_pause = 0.000000000000001
pause = False
end = False
while running:
    shape.m_down(screen)
    clock.tick(fps)
    k = 0

    for i in range(len(shape.field)):
        if shape.field[i] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
            del shape.field[i]
            shape.field.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            shape.record += 10
            if shape.max_record[0][0] < shape.record:
                shape.cursor.execute("DELETE FROM records WHERE ID = 1")
                shape.cursor.execute("INSERT INTO records (ID, num) VALUES (1, {})".format(shape.record))
                shape.max_record = shape.cursor.execute("""SELECT num FROM records""").fetchall()
                shape.conn.commit()
            print('           ', shape.record)

    if 1 in shape.field[0]:
        print(111111111111111)
        f1 = pygame.font.Font(None, 50)
        text5 = f1.render('GAME OVER!', True,
                          (255, 255, 255))
        screen.blit(text5, (500, 450))
        text6 = f1.render('PRESS R TO RESTART!', True,
                          (255, 255, 255))
        screen.blit(text6, (410, 500))
        fps = 5
        end = True


    # for i in range(k):
    #     shape.field.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            coords = event.pos
            if coords[0] > board.width * board.cell_size or coords[1] > board.height * board.cell_size:
                print("None")
            else:
                coords_r = (coords[0] - 10) // board.cell_size
                coords_rr = (coords[1] - 10) // board.cell_size
                print((coords_r, coords_rr))
                for i in range(coords_r):

                    for j in range(coords_rr):
                        pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                shape.rotate(screen)
            if event.key == pygame.K_RIGHT:
                shape.m_right(screen)
            if event.key == pygame.K_DOWN:
                shape.m_down(screen)
            if event.key == pygame.K_LEFT:
                shape.m_left(screen)
            if event.key == pygame.K_SPACE:
                while shape.stop:
                    shape.m_down(screen)
            if event.key == pygame.K_r:
                end = False
                board = Board(10, 20)
                shape = Shape()
                shape.choose()
                shape.draw_s(screen)
                clock = pygame.time.Clock()



    #if int(shape.record) > int(shape.max_record):
    #    max_record = open('record.txt', 'w')
    #    max_record.write(str(shape.record))
    #    max_record.close()

    f1 = pygame.font.Font(None, 50)
    text1 = f1.render('Record:', True,
                      (255, 255, 255))
    screen.blit(text1, (500, 100))
    text2 = f1.render(str(shape.record), True,
                      (255, 255, 255))
    screen.blit(text2, (550, 150))
    text3 = f1.render('Max Record:', True,
                      (255, 255, 255))
    screen.blit(text3, (500, 300))
    text4 = f1.render(str(shape.max_record[0][0]), True,
                      (255, 255, 255))
    screen.blit(text4, (550, 350))
    #screen.blit(board.fon, (0, 0))
            #if event.key == pygame.K_ESCAPE:
            #    if pause == False:
            #        print('                 ', 'PAUSED')
            #        fps_pause = fps
            #        fps = 0.000000000000001
            #        pause = True
            #    elif pause == True:
            #        print('                 ', 'CONTINUED')
            #        fps = fps_pause
            #        fps_pause = 0.000000000000001
            #        pause = False
    # screen.fill((40, 40, 40))
    board.render(screen)
    pygame.display.flip()