import pygame
import argparse
import random

FPS = 30

LEFT = 1  # left mouse button
MIDDLE = 2
RIGHT = 3  # ...
WHEELUP = 4
WHEELDOWN = 5

WIDTH = 1000
HEIGHT = 1000
RESOLUTION = (WIDTH, HEIGHT)
NUM_PEOPLE = 10


class Person:
    '''
    A person trying to form a triangle with two other random
    persons
    '''

    def __init__(self, pos_x, pos_y, size=10):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size

    def setup(self, people):
        '''
        Pick two random partners and memorize
        Called after people have been initialized
        '''
        without_me = [p for p in people if p is not self]
        assert len(without_me) >= 2, 'Not enough people!'
        person_a, person_b = random.sample(without_me, 2)
        self.pa = person_a
        self.pb = person_b

    def move(self, dt):
        '''
        Moving magic happens here. Random for now ...
        '''
        self.pos_x += random.uniform(-2, 2)
        self.pos_y += random.uniform(-2, 2)

    def draw(self, display):
        '''
        Create a surface and draw yourself on display
        Do not care for colors
        '''

        red = 0
        green = 255
        blue = 0

        surface = pygame.Surface(
            (self.size, self.size)
        )

        pygame.draw.rect(
            surface,
            (red, green, blue, 0),
            (0, 0, self.size, self.size),
        )

        surface = surface.convert_alpha()
        display.blit(surface, (self.pos_x, self.pos_y))


def main():

    pygame.init()

    screen = pygame.display.set_mode(RESOLUTION)

    pygame.display.set_caption("TrianglePeople")
    pygame.mouse.set_visible(1)

    clock = pygame.time.Clock()
    running = True

    # prepare people
    people = [
        Person(
            pos_x=random.randint(0, WIDTH),
            pos_y=random.randint(0, HEIGHT),
        )
        for _ in range(NUM_PEOPLE)
    ]
    for person in people:
        person.setup(people)

    # main loop
    while running:

        dt = clock.tick(FPS)

        background = pygame.Surface(RESOLUTION)
        background.fill((0, 0, 0, 0))
        background = background.convert_alpha()

        # temporary surface to draw things to
        display = pygame.Surface(RESOLUTION)
        display.fill((0, 0, 0, 0))
        display = display.convert_alpha()
        display.blit(background, (0, 0))

        for person in people:
            person.move(dt)
            person.draw(display)

        screen.blit(display, (0, 0))

        pygame.display.flip()

        # look for events
        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                print('Quitting!')
                pygame.quit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                print('left mouse button')

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                print('right mouse button')

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    pass
                else:
                    pass


if __name__ == '__main__':
    main()
