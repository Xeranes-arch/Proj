"""
A simple physics simulation representing a Trebuchet.
The User is able to place a ball, set its initial velocity and launch it, attempting to hit a target.
"""

import pymunk
import pymunk.pygame_util
import pygame
import sys

from pymunk.vec2d import Vec2d


def main():
    
    print("This is GOT. \nYou place the ball, set its launch direction and initial speed as well as reset by left clicking. \nGot it? Let's go.")

    # Define screen
    size = (1280, 720)
    pts = [(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])]
    screen = pygame.display.set_mode(size)

    space = create_World(pts)
    run(screen, space)


def create_World(pts):
    """creates the environment of the game"""
    # Make space
    space = pymunk.Space()
    space.gravity = (0, 981)

    # Make world boundaries
    for i in range(4):
        segment = pymunk.Segment(
            space.static_body, pts[i], pts[(i+1) % 4], 4)
        segment.elasticity = 0.75
        segment.friction = 0.75
        space.add(segment)

    # Make target
    for i in range(2):
        t = pymunk.Segment(space.static_body, (940 + 60 * i, 720), (940 + 60 * i, 320), 2)
        t.elasticity = 0.75
        t.friction = 0.75
        space.add(t)
    return space


def run(screen, space):
    """Run it."""
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # Loop flags / one could do without them and just use n, but for the sake of readabillity, flags
    n = 0
    flag = {"run": True, "winable": False, "simulate": False}

    while run:

        # Check for inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # First click
                if n == 0:
                    place_ball(space, pos)
                    flag["winable"] = True
                    n += 1
                # Second click
                elif n == 1:
                    set_dirandvel(space, pos)
                    flag["simulate"] = True
                    n += 1
                # Third click
                elif n == 2:
                    reset(space)
                    flag["simulate"] = False
                    n = 0

        screen.fill((210, 210, 210))
        if n == 1:
            line = [pos, pygame.mouse.get_pos()]
            pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 3)
        space.debug_draw(draw_options)
        pygame.display.update()

        # Only simulate ball once user clicks second time
        if flag["simulate"]:

            # Rolling friction / for whatever reason, if allowed to apply in the air it will dampen way too much.
            if space.body.position[1] > 696:
                space.body.angular_velocity *= 0.975

            space.step(0.001)

            # Check win
            if 940 < (space.body.position)[0] < 1000 and space.body.position[1] > 696 and flag["winable"]:
                print("You win! \nGo again if you like.")
                flag["winable"] = False


def place_ball(space, pos):
    """Places ball at given click position."""
    space.body = pymunk.Body(mass=1, moment=10)
    space.body.position = pos
    space.ball = pymunk.Circle(space.body, radius=20)
    space.ball.elasticity = 0.5
    space.ball.friction = 0.75
    space.add(space.body, space.ball)


def set_dirandvel(space, pos):
    """Sets initial impulse."""
    p0 = space.body.position
    x, y = pos
    p1 = Vec2d(x=float(x), y=float(y))
    impulse = 10 * (p1 - p0)
    space.body.apply_impulse_at_local_point(impulse)


def reset(space):
    """Removes previous ball."""
    space.remove(space.body)
    space.remove(space.ball)


if __name__ == "__main__":
    main()
