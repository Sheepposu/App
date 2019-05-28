import pygame, random, time, sys, threading, pickle
from PyGameFuncs import Button as BT, Screen_Display as SD

pygame.init()
Screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

fps = 100
speed = -1
tubeList = []
playing = True
tubeSpeed = 1

def Save(score):
    file = open('FlappyBirdData.txt', 'wb')
    pickle.dump(score, file)
    file.close()

Save(0)

def Load():
    file = open('FlappyBirdData.txt', 'rb')
    return pickle.load(file)

def TubeCreate():
    global tubeSpeed
    count = 0
    sleep = 3
    while playing:
        time.sleep(sleep)
        count += 1
        tubeList.append(Tube())
        if count == 10:
            tubeSpeed += 1
            sleep -= 1
            count = 0

def speedChange():
    global speed
    while True:
        time.sleep(.2)
        if speed > -5:
            speed -= 1

class Bird():
    def __init__(self):
        self.rect = pygame.Rect(100, 300, 17, 13)
        self.image = pygame.image.load('Bird.png')
        self.debounce = False

    def draw(self):
        Screen.blit(self.image, (self.rect[0], self.rect[1]))

    def move(self):
        global speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keyed = pygame.key.get_pressed()
        if keyed[pygame.K_SPACE] == 1 and not self.debounce:
            self.debounce = True
            speed = 2
        elif keyed[pygame.K_SPACE] == 0 and self.debounce:
            self.debounce = False
            
        self.rect = pygame.Rect(self.rect[0], self.rect[1] - speed, self.rect[2], self.rect[3])

    def main(self):
        self.draw()
        self.move()

class Tube():
    def __init__(self):
        self.topRect = pygame.Rect(700, random.randint(-200, 0), 50, 400)
        self.bottomRect = pygame.Rect(700, self.topRect[1] + 500, 50, 400)

    def draw(self):
        pygame.draw.rect(Screen, (0, 200, 0), (self.topRect))
        pygame.draw.rect(Screen, (0, 200, 0), (self.bottomRect))

    def move(self):
        self.topRect = pygame.Rect(self.topRect[0] - tubeSpeed, self.topRect[1], self.topRect[2], self.topRect[3])
        self.bottomRect = pygame.Rect(self.bottomRect[0] - tubeSpeed, self.bottomRect[1], self.bottomRect[2], self.bottomRect[3])

    def main(self):
        self.draw()
        self.move()

def StartMenu():
    while True:
        Screen.fill((0, 255, 0))
        SD.message_display(Screen, 'Press Enter/Return to Play!', 60, (0, 0, 255), 400, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keyed = pygame.key.get_pressed()
        if keyed[pygame.K_RETURN]:
            break
        pygame.display.update()
        clock.tick(20)

def Main():
    global playing
    score = 0
    highscore = Load()
    StartMenu()
    plr = Bird()
    t1 = threading.Thread(target=speedChange)
    t3 = threading.Thread(target=TubeCreate)
    t3.start()
    t1.start()
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
        Screen.fill((0, 0, 255))
        t2 = threading.Thread(target=plr.main)
        t2.start()
        for tube in tubeList:
            t4 = threading.Thread(target=tube.main)
            t4.start()
            if plr.rect.colliderect(tube.topRect) or plr.rect.colliderect(tube.bottomRect) or plr.rect[1] + plr.rect[3] >= 600:
                playing = False
            if tube.topRect[0] <= 50:
                score += 1
                if score > highscore:
                    highscore = score
                    Save(highscore)
                tubeList.remove(tube)
        SD.message_display(Screen, 'Highscore: %s' %highscore, 40, (255, 0, 0), 700, 30)
        SD.message_display(Screen, 'Score: %s' %score, 40, (255, 0, 0), 75, 30)
        pygame.display.update() 
        clock.tick(fps)
    

Main()
SD.message_display(Screen, 'Game Over!', 100, (255, 0, 0), 400, 300)
pygame.display.update()
time.sleep(3)
pygame.quit()
sys.exit()
