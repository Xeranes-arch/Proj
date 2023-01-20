import pymunk
import pymunk.pygame_util
import pygame

from pymunk.vec2d import Vec2d


def main():
    print("This is GOT. \nYou place the ball, set its launch direction and initial speed as well as reset by left clicking. \nGot it? Let's go.")
    # define screen
    size = (1280, 720)
    pts = [(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])]
    screen = pygame.display.set_mode(size)
    space = create_World(pts)
    run(screen, space)


def create_World(pts):
    """creates the environment of the game"""
    # make space
    space = pymunk.Space()
    space.gravity = (0, 981)
    # make world boundaries
    for i in range(4):
        segment = pymunk.Segment(
            space.static_body, pts[i], pts[(i+1) % 4], 4)
        segment.elasticity = 0.75
        segment.friction = 0.75
        space.add(segment)
    # make target
    t1 = pymunk.Segment(space.static_body,
                        (940, 720), (940, 320), 2)
    t1.elasticity = 0.75
    t1.friction = 0.75
    t2 = pymunk.Segment(space.static_body,
                        (1000, 720), (1000, 320), 2)
    t2.elasticity = 0.75
    t2.friction = 0.75
    space.add(t1, t2)
    return space


def run(screen, space):
    """Well. It runs the game."""
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    # loop flags / one could do without them and just use n, but for the sake of readabillity, flags
    n = 0
    update = False
    winable = False
    run = True
    # Interface starts running
    while run:
        screen.fill((210, 210, 210))
        # check inputs
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                run = False
            # mouseclick; first, second, third, fourth
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if n == 0:
                    place_ball(space, pos)
                    winable = True
                    n += 1
                elif n == 1:
                    set_dirandvel(space, pos)
                    n += 1
                    update = True
                elif n == 2:
                    reset(space)
                    update = False
                    n = 0
        # Vector dirandvel
        if n == 1:
            line = [pos, pygame.mouse.get_pos()]
            pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 3)
        space.debug_draw(draw_options)
        pygame.display.update()
        # only run once user launches/clicks second time
        if update:
            # rolling friction / for whatever reason, if allowed to apply in the air it will dampen way too much.
            if space.body.position[1] > 696:
                space.body.angular_velocity *= 0.975
            space.step(0.001)
            if 940 < (space.body.position)[0] < 1000 and space.body.position[1] > 696 and winable:
                print("You win! \nGo again if you like.")
                winable = False


def place_ball(space, pos):
    """places ball at given click position"""
    space.body = pymunk.Body(mass=1, moment=10)
    space.body.position = pos
    space.ball = pymunk.Circle(space.body, radius=20)
    space.ball.elasticity = 0.5
    space.ball.friction = 0.75
    space.add(space.body, space.ball)


def set_dirandvel(space, pos):
    """should draw arrow to click and wait """
    p0 = space.body.position
    x, y = pos
    p1 = Vec2d(x=float(x), y=float(y))
    impulse = 10 * (p1 - p0)
    space.body.apply_impulse_at_local_point(impulse)


def reset(space):
    """removes previous ball"""
    space.remove(space.body)
    space.remove(space.ball)


if __name__ == "__main__":
    main()
