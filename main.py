import pygame
import sys
from pygame.locals import *
import time

class Player:
    def __init__(self, filename, filename2, cols):
        self.sheet = pygame.image.load(filename)
        self.sheet2 = pygame.image.load(filename2)

        self.cols = cols
        self.rows = 1

        self.rect = self.sheet.get_rect()
        self.rect2 = self.sheet2.get_rect()
        w = self.cellWidth = self.rect.width / cols
        h = self.cellHeight = self.rect.height / self.rows
        hw, hh = self.cellCenter = (w / 2, h / 2)

        self.cells = list([(index % cols * w, index // cols * h, w, h) for index in range(cols)])
        self.idle = [self.cells[0], self.cells[1], self.cells[2], self.cells[3]]
        self.move = [self.cells[4], self.cells[5], self.cells[6], self.cells[7], self.cells[8], self.cells[9]]
        self.sprint = [self.cells[17], self.cells[18], self.cells[19], self.cells[20], self.cells[21], self.cells[22], self.cells[23]]
        self.idle_left = [self.cells[23], self.cells[22], self.cells[21], self.cells[20]]
        self.move_left = [self.cells[19], self.cells[18], self.cells[17], self.cells[16], self.cells[15], self.cells[14]]
        self.sprint_left = [self.cells[6], self.cells[5], self.cells[4], self.cells[3], self.cells[2], self.cells[1], self.cells[0]]
        self.handle = list([(0,0), (-hw, 0), (-w, 0), (0, -hh), (-hw, -hh), (-w, -hh), (0, -h),
            (-hw, -h), (-w, -h)])

    def draw_idle(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.idle[cellIndex])

    def draw_move(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.move[cellIndex])
    
    def draw_sprint(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet, (x + self.handle[handle][0], y + self.handle[handle][1]), self.sprint[cellIndex])

    def draw_idle_left(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet2, (x + self.handle[handle][0], y + self.handle[handle][1]), self.idle_left[cellIndex])

    def draw_move_left(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet2, (x + self.handle[handle][0], y + self.handle[handle][1]), self.move_left[cellIndex])

    def draw_sprint_left(self, surface, cellIndex, x, y, handle = 0):
        surface.blit(self.sheet2, (x + self.handle[handle][0], y + self.handle[handle][1]), self.sprint_left[cellIndex])

walkCount = 0
sprintCount = 0
nextSprint = time.time()
nextWalk = time.time()

def redrawGameWindow(screen, background, player, playerPos, frame, right, left, idle, prev, sprint):
    global walkCount
    global nextWalk
    global sprintCount
    global nextSprint

    screen.blit(background, (0,0))  # This will draw our background image at (0,0)

    if right:
        if sprint:
            player.draw_sprint(screen, sprintCount, playerPos[0], playerPos[1], 4)
            if time.time() > nextSprint:
                sprintCount = (sprintCount + 1) % 7
                nextSprint = time.time() + 0.04
        else:
            player.draw_move(screen, walkCount, playerPos[0], playerPos[1], 4)
            if time.time() > nextWalk:
                walkCount = (walkCount + 1) % 6
                nextWalk = time.time() + 0.08
    elif left:
        if sprint:
            player.draw_sprint_left(screen, sprintCount, playerPos[0], playerPos[1], 4)
            if time.time() > nextSprint:
                sprintCount = (sprintCount + 1) % 7
                nextSprint = time.time() + 0.04
        else:
            player.draw_move_left(screen, walkCount, playerPos[0], playerPos[1], 4)
            if time.time() > nextWalk:
                walkCount = (walkCount + 1) % 6
                nextWalk = time.time() + 0.08
    elif idle and prev == "RIGHT":
        player.draw_idle(screen, frame, playerPos[0], playerPos[1], 4)
        walkCount = 0
        sprintcount = 0
    elif idle and prev == "LEFT":
        player.draw_idle_left(screen, frame, playerPos[0], playerPos[1], 4)
        walkCount = 0
        sprintCount = 0

    pygame.display.update()

def main():
    # Initialise display
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('A Python Game')
    clock = pygame.time.Clock()
    FPS = 60

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    # Initialise player
    player = Player("assets/player.png", "assets/player_left.png", 24)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Frame variables
    nextFrame = time.time()
    frame = 0
    playerPos = [400, 300]
    right = False
    left = False
    prev = "RIGHT"
    idle = True
    sprint = False

    # Event loop
    while 1:

        # FPS
        clock.tick(FPS)

        keys=pygame.key.get_pressed()
        if keys[K_RIGHT]:
            if keys[K_LSHIFT]:
                playerPos[0] += 1.2
                if playerPos[0] > 810:
                    playerPos[0] = 0
                right = True
                left = False
                idle = False
                sprint = True
            else:
                playerPos[0] += 0.75
                if playerPos[0] > 820:
                    playerPos[0] = 0
                right = True
                left = False
                idle = False
                sprint = False
        elif keys[K_LEFT]:
            if keys[K_LSHIFT]:
                playerPos[0] -= 1.2
                if playerPos[0] < -10:
                    playerPos[0] = 800
                right = False
                left = True
                idle = False
                sprint = True
            else:
                playerPos[0] -= 0.75
                if playerPos[0] < -20:
                    playerPos[0] = 800
                left = True
                right = False
                idle = False
                sprint = False
        else:
            if right == True:
                prev = "RIGHT"
            elif left == True:
                prev = "LEFT"
            right = False
            left = False
            idle = True
            sprint = False
            walkCount = 0
            sprintCount = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        if time.time() > nextFrame:
            frame = (frame + 1) % 4
            nextFrame = time.time() + 0.25

        redrawGameWindow(screen, background, player, playerPos, frame, right, left, idle, prev, sprint)

if __name__ == '__main__':
    main()
