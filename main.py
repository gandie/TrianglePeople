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
RED = (255, 0, 0, 0)
GREEN = (0, 255, 0, 0)
BLUE = (0, 0, 255, 0)


class Person:
    '''
    A person trying to form an equilateral triangle with two other random
    persons
    '''

    def __init__(self, pos_x, pos_y, size=10, speed=1):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.speed = 1 / FPS
        self.color = BLUE

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
        Clumsy ugly movement magic happens here.
        Called each tick
        Calculate closest target point to form equilateral triangle with
        partners, slow down when close to target
        '''

        if random.random() < 0.5:
            return

        me = pygame.math.Vector2(
            self.pos_x,
            self.pos_y,
        )

        va = pygame.math.Vector2(
            self.pa.pos_x,
            self.pa.pos_y,
        )

        vb = pygame.math.Vector2(
            self.pb.pos_x,
            self.pb.pos_y,
        )

        ab = vb - va
        rot_ab_left = ab.copy().normalize().rotate(90)
        rot_ab_right = ab.copy().normalize().rotate(-90)

        triangle_sl = ab.length()
        triangle_height = (triangle_sl / 2) * (3 ** 0.5)

        target_left = va + 0.5 * ab + rot_ab_left * triangle_height
        target_right = va + 0.5 * ab + rot_ab_right * triangle_height

        to_target_left = target_left - me
        to_target_right = target_right - me

        if to_target_left.length() < to_target_right.length():
            to_target = to_target_left
        else:
            to_target = to_target_right

        err = to_target.copy().length()

        if err < 10 and self.speed > 0.0005:
            self.speed *= 0.9

        if err > 100:
            self.speed = 1 / FPS

        if err < 0.01:
            print('match!')
            self.color = GREEN
            return

        self.color = BLUE
        to_target_norm = to_target.copy().normalize()

        self.pos_x += to_target_norm.x * self.speed * dt
        self.pos_y += to_target_norm.y * self.speed * dt

    def draw(self, display):
        '''
        Create a surface and draw yourself on display
        Do not care for colors
        Called each tick after movement
        '''

        red = 0
        green = 255
        blue = 0

        surface = pygame.Surface(
            (self.size, self.size)
        )

        pygame.draw.rect(
            surface,
            self.color,
            (0, 0, self.size, self.size),
        )

        surface = surface.convert_alpha()
        display.blit(surface, (self.pos_x, self.pos_y))


def setup_people(args):
    # prepare people
    people = [
        Person(
            pos_x=random.randint(int((1/3)*WIDTH), int((2/3)*WIDTH)),
            pos_y=random.randint(int((1/3)*HEIGHT), int((2/3)*HEIGHT)),
        )
        for _ in range(args.num_people)
    ]
    for person in people:
        person.setup(people)
    return people


def main(args):

    pygame.init()

    screen = pygame.display.set_mode(RESOLUTION)

    pygame.display.set_caption("TrianglePeople")
    pygame.mouse.set_visible(1)

    clock = pygame.time.Clock()
    running = True

    people = setup_people(args)

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
                    people = setup_people(args)
                    print(8)
                else:
                    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser('TrianglePeople')
    parser.add_argument(
        'num_people',
        help='Number of people to involve. Default is 5',
        type=int,
        default=5
    )

    args = parser.parse_args()

    main(args)
