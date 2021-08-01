import pygame
import random


class Cube(object):
    win_size = 500
    grid_div = 20

    def __init__(self, position, direction_x=0, direction_y=0, color=(0, 255, 0)):
        self.position = position
        self.direction_x = 0
        self.direction_y = 0
        self.color = color

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y

        self.position = (self.position[0] + self.direction_x, self.position[1] + self.direction_y)

    def draw(self, surface, head=False):
        space = round(self.win_size / self.grid_div)
        x = self.position[0]
        y = self.position[1]

        if head:
            pygame.draw.rect(window, (0, 180, 0), (x * space, y * space, space, space))
        else:
            pygame.draw.rect(window, self.color, (x * space, y * space, space, space))


class Snake(object):
    body = []  # the body is a list of cubes
    turns = {}

    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.head = Cube(self.position)
        self.body.append(self.head)  # we make the snake longer by appending cubes to the body list
        self.direction_x = 0
        self.direction_y = -1

    def move(self, key):
        if key[pygame.K_UP] and self.direction_y != 1:
            self.direction_y = -1
            self.direction_x = 0
            self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]  # logs the direction the head turned

        elif key[pygame.K_DOWN] and self.direction_y != -1:
            self.direction_y = 1
            self.direction_x = 0
            self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

        elif key[pygame.K_LEFT] and self.direction_x != 1:
            self.direction_x = -1
            self.direction_y = 0
            self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

        elif key[pygame.K_RIGHT] and self.direction_x != -1:
            self.direction_x = 1
            self.direction_y = 0
            self.turns[self.head.position[:]] = [self.direction_x, self.direction_y]

        for i, c in enumerate(self.body):  # for the number of cube objects in the body list
            p = c.position[:]  # take the position of the current cube object
            if p in self.turns:  # if a turn was made at that position earlier
                turn = self.turns[p]  # get the direction_x and direction_y of the turn at that position
                c.move(turn[0], turn[1])  # turn
                if i == len(self.body) - 1:  # if that was the last cube in the body
                    self.turns.pop(p)  # remove that turn position form the list

            else:  # if nothing is being pressed (the snake is constantly moving regardless)
                if (c.direction_x == -1) and (c.position[0] <= -1):  # left side
                    self.reset((10, 10))

                elif (c.direction_x == 1) and (c.position[0] >= c.grid_div - 1):  # right side
                    self.reset((10, 10))

                elif (c.direction_y == -1) and (c.position[1] <= 0):  # up
                    self.reset((10, 10))

                elif (c.direction_y == 1) and (c.position[1] >= c.grid_div):  # down
                    self.reset((10, 10))

                else:
                    c.move(c.direction_x, c.direction_y)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:  # checks if this is the head
                c.draw(surface, True)

            else:
                c.draw(surface)

    def add_cube(self):
        tail = self.body[-1]  # check last item in list
        dx, dy = tail.direction_x, tail.direction_y

        if (dx == 1) and (dy == 0):
            self.body.append(Cube((tail.position[0] - 1, tail.position[1])))

        elif (dx == -1) and (dy == 0):
            self.body.append(Cube((tail.position[0] + 1, tail.position[1])))

        elif (dx == 0) and (dy == 1):
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))

        elif (dx == 0) and (dy == - 1):
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))

        self.body[-1].direction_x = dx  # set the new cube moving in the same direction as the others
        self.body[-1].direction_y = dy

    def reset(self, position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 0


def draw_grid(win_size, grid_div, surface):
    space = round(win_size / grid_div)

    x, y = 0, 0
    for r in range(grid_div):
        x += space
        y += space

        # comment this part out later
        # pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, size), 1)  # vertical lines
        # pygame.draw.line(surface, (255, 255, 255), (0, y), (size, y), 1)  # horizontal lines


def random_apple(grid_div, snake_object):
    positions = snake.body

    while True:
        x = random.randrange(grid_div)
        y = random.randrange(grid_div)

        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0:  # checks the snake list so that the apple does not appear on top of the snake
            continue
        else:
            break

    return x, y


# window and frame rate setup
pygame.display.set_caption("Snake")
icon = pygame.image.load("assets\\icon.png")
pygame.display.set_icon(icon)
size = 500
div = int(size / 25)  # on a 500x500 window, this is a 20x20 grid
window = pygame.display.set_mode((size, size))
clock = pygame.time.Clock()

# object initialization
snake = Snake((225, 0, 0), (10, 10))
apple = Cube(random_apple(div, snake), color=(255, 0, 0))

body = []

still_playing = True
while still_playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    window.fill((0, 0, 0))
    draw_grid(size, div, window)
    apple.draw(window)

    if snake.body[0].position == apple.position:
        snake.add_cube()
        apple = Cube(random_apple(div, snake), color=(255, 0, 0))

    for x in range(len(snake.body)):  # i hate this i hate this i hate this i hate this i hate this i hate this i hate t
        try:
            if snake.body[x].position in list(map(lambda z: z.position, snake.body[x + 1:])):
                snake.reset((10, 10))
                apple = Cube(random_apple(div, snake), color=(255, 0, 0))
                apple.draw(window)
        except IndexError:
            pass

    if snake.body[0] in body:
        snake.reset((10, 10))

    key_pressed = pygame.key.get_pressed()
    snake.move(key_pressed)
    snake.draw(window)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
