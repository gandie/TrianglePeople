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

SEED = 'dunkelschwarzerheisserkaffee'


class Person:
    '''
    A person trying to form an equilateral triangle with two other random
    persons
    '''

    def __init__(self, pos_x, pos_y, size=3, err_tol=5):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.err_tol = err_tol

        self.speed = 1 / FPS
        self.color = BLUE
        self.match = False

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
        to_target_norm = to_target.copy().normalize()

        if err < 2 * (self.err_tol ** 0.5) and self.speed > 0.01:
            self.speed *= 0.9

        if err > 2 * (self.err_tol ** 0.5):
            self.speed = 1 / FPS

        if err < self.err_tol:
            self.match = True
            return

        self.match = False

        if random.random() < 0.5:
            self.pos_x += to_target_norm.x * self.speed * dt
            self.pos_y += to_target_norm.y * self.speed * dt

    def draw(self, display):
        '''
        Create a surface and draw yourself on display
        Called each tick after movement
        '''

        surface = pygame.Surface(
            (self.size, self.size)
        )

        pygame.draw.rect(
            surface,
            GREEN if self.match else BLUE,
            (0, 0, self.size, self.size),
        )

        surface = surface.convert_alpha()
        display.blit(surface, (self.pos_x, self.pos_y))


def setup_people(args):
    '''
    Create list of people and call setup method afterwards
    '''
    people = [
        Person(
            pos_x=random.randint(int((1/3)*WIDTH), int((2/3)*WIDTH)),
            pos_y=random.randint(int((1/3)*HEIGHT), int((2/3)*HEIGHT)),
            err_tol=args.err_tol,
        )
        for _ in range(args.num_people)
    ]
    for person in people:
        person.setup(people)
    return people


def main(args):

    if args.seed:
        print('Using given seed: %s' % args.seed)
        random.seed(args.seed)
    else:
        print('Using default seed: %s' % SEED)
        random.seed(SEED)

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

        for person in people:
            if person.match:
                pygame.draw.line(
                    screen,
                    GREEN,
                    (person.pos_x, person.pos_y),
                    (person.pa.pos_x, person.pa.pos_y),
                    width=1,
                )
                pygame.draw.line(
                    screen,
                    GREEN,
                    (person.pos_x, person.pos_y),
                    (person.pb.pos_x, person.pb.pos_y),
                    width=1,
                )

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
                    args.num_people += 1
                    print('num_people: %s' % args.num_people)
                elif event.key == pygame.K_DOWN:
                    if args.num_people > 3:
                        args.num_people -= 1
                        print('num_people: %s' % args.num_people)
                elif event.key == pygame.K_LEFT:
                    args.err_tol -= 1
                    print('err_tol: %s' % args.err_tol)
                elif event.key == pygame.K_RIGHT:
                    args.err_tol += 1
                    print('err_tol: %s' % args.err_tol)
                elif event.key == pygame.K_BACKSPACE:
                    people = setup_people(args)
                else:
                    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser('TrianglePeople')
    parser.add_argument(
        'num_people',
        help='Number of people to involve',
        type=int,
    )

    parser.add_argument(
        '-s',
        '--seed',
        help='Random seed to use',
        type=str,
    )

    parser.add_argument(
        '-e',
        '--err_tol',
        help='Error tolerance. Default is 5',
        type=int,
        default=5
    )

    args = parser.parse_args()

    main(args)
