import pygame
import os
import random
import time
import itertools
import webbrowser

def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname)
    return image


gameover = load_image("gameover.jpg")
choose = load_image("choose.png")
scoreboard = load_image("scoreboard.jpg")
start_screen = load_image("start_screen.jpg")
start = load_image("start.png")
curs = load_image("arrow.png")
stop = load_image("stop.png")
track = load_image("background.jpg")
car = load_image("porsche.png")
pygame.init()
width, height = 1024, 768
size = width, height
screen = pygame.display.set_mode(size)
running = True
gamming = False
pygame.mouse.set_visible(False)
list_car_pos = [80, 235, 395, 550]
list_stop_pos = [185, 335, 495, 650]
car_pos = 0
avaria = 0
y_pos = -1050
x_pos = -768
v1 = 300
score = 0
ti = 0
last_ti = 0
level = 1
last_gen = []


def draw_problems(time1):
    global problems
    global avaria
    global ti
    global score
    global last_ti
    global level
    global last_gen
    ti += time1
    if ti - last_ti >= 400:
        gen = random.choice(list(itertools.combinations([1, 2, 3, 4], random.choice([1, 2, 3]))))
        gen = list(gen)
        gen.sort()
        if level == 1 or level == 2:
            while (gen == [1, 2, 3] and last_gen == [2, 3, 4]) or (gen == [2, 3, 4] and last_gen == [1, 2, 3]):
                gen = random.choice(list(itertools.combinations([1, 2, 3, 4], random.choice([1, 2, 3]))))
        last_gen = gen[:]
        for i in gen:
            problems.append([i - 1, -100])
            last_ti = ti
    for i in range(len(problems)):
        problems[i][1] += time1
    del_list = []
    for i in range(len(problems)):
        screen.blit(stop, (list_stop_pos[problems[i][0]], problems[i][1]))
        if problems[i][1] > 720:
            del_list.append(i)
        if problems[i][0] == car_pos and problems[i][1] > 400 and problems[i][1] < 680:
            avaria = 1  
            f = open('record.txt', 'r')
            y = f.read()
            f.close()
            if int(float(score)) > int(y):
                f = open('record.txt', 'w')
                f.write(str(int(float(score))))
                f.close()
    del_list = del_list[::-1]
    for i in del_list:
        del problems[i]
    score += time1/10
    
while running:
    if gamming == True:
        clock = pygame.time.Clock();
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                l = event.scancode
                if l == 77 and car_pos <= 2 and avaria == 0:
                    car_pos += 1
                if l == 75 and car_pos >= 1 and avaria == 0:
                    car_pos -= 1
                if l == 72 and level == 2:
                    v += 10
                if l == 1:
                    gamming = False
                if l == 33:
                    webbrowser.open_new('https://money.yandex.ru/to/410014391030188')
        screen.fill((255, 255, 255))
        screen.blit(track, (0,0))
        screen.blit(car, (list_car_pos[car_pos], 530))
        if avaria == 0:
            draw_problems(v / 1000 * clock.tick())
        else:
            draw_problems(0)
            if x_pos <= 0 and y_pos <= 0:
                x_pos += v1 * clock.tick() / 1000 
                y_pos = x_pos
            screen.blit(gameover, (x_pos, -1* y_pos))       
        if pygame.mouse.get_focused() == 1:
                screen.blit(curs, pygame.mouse.get_pos()) 
        screen.blit(scoreboard, (0, 0))
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('score: ' + str(int(score)), 1, (255, 255, 255)) 
        screen.blit(text1, (0, 0))
        pygame.display.flip()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()  
                if x < 280 and x > 45 and y < 665 and y > 580:
                    car_pos = 0
                    if level == 1:
                        v = 300
                    elif level == 2:
                        v = 500
                    elif level == 3:
                        v = 500 
                    y_pos = -1024
                    x_pos = -768                  
                    avaria = 0
                    ti = 0
                    score = 0
                    last_gen = []
                    last_ti = 0                    
                    problems = [[0, 0], [1, 0], [3, 0]]
                    gamming = True
                elif x > 65 and x < 140 and y > 480 and y < 530:
                    level = 1
                elif x > 150 and x < 210 and y > 480 and y < 530:
                    level = 2
                elif x > 215 and x < 290 and y > 480 and y < 530:
                    level = 3        
            if event.type == pygame.KEYDOWN:
                l = event.scancode
                if l == 28:
                    car_pos = 0
                    if level == 1:
                        v = 300
                    elif level == 2:
                        v = 500
                    elif level == 3:
                        v = 500  
                    last_gen = []
                    score = 0
                    avaria = 0
                    y_pos = -1024
                    x_pos = -768
                    ti = 0
                    last_ti = 0                    
                    problems = [[0, 0], [1, 0], [3, 0]]
                    gamming = True
                if l == 1:
                    running = False
        screen.fill((255, 255, 255))
        screen.blit(start_screen, (0, 0))
        f = open('record.txt', 'r')
        record = f.read()
        f.close()
        f1 = pygame.font.Font(None, 36)
        text1 = f1.render('record: ' + str(record), 1, (0, 0, 0)) 
        screen.blit(text1, (0, 0))        
        screen.blit(start, (50, 550))
        screen.blit(choose, (45, 400))
        if pygame.mouse.get_focused() == 1:
                screen.blit(curs, pygame.mouse.get_pos())   
        pygame.display.flip()        
pygame.quit()
