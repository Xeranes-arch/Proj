import pymunk
import pymunk.pygame_util
import pygame
import random

import pymunk.shapes
from pymunk.vec2d import Vec2d


def main():
    print("This is GOT. \nYou place the ball, set its launch direction and initial speed as well as reset by left clicking. \nGot it? Let's go. Press Enter to start:")
    # input()
    # init pygame with world ready to play
    world = World()
    world.run()


class World:

    def __init__(self):
        # define screen
        size = (1280, 720)
        pts = [(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])]
        wind = random.randint(-500, 500)
        self.screen = pygame.display.set_mode(size)
        # create space
        self.space = pymunk.Space()
        self.space.gravity = (wind, 981)
        # make world boundaries
        for i in range(4):
            segment = pymunk.Segment(
                self.space.static_body, pts[i], pts[(i+1) % 4], 4)
            segment.elasticity = 0.75
            segment.friction = 0.75
            self.space.add(segment)
        # make random box target
        self.t = None
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.make_target()
        # ball
        self.body = None
        self.ball = None

    def run(self):
        """Well. It runs the game."""
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        # loop flags / one could do without them and just use n, but for the sake of readabillity, flags
        n = 0
        update = False
        winable = False
        run = True
        won = False
        # Interface starts running
        while run:
            self.screen.fill((210, 210, 210))
            # check inputs
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    run = False
                # mouseclick; first, second, third, fourth
                if event.type == pygame.MOUSEBUTTONDOWN:
                    ball_pos = pygame.mouse.get_pos()
                    if n == 0:
                        self.place_ball(ball_pos)
                        winable = True
                        n += 1
                    elif n == 1:
                        self.set_dirandvel(ball_pos)
                        n += 1
                        update = True
                    elif n == 2:
                        self.reset()
                        update = False
                        n = 0
                        # new target
                        if won:
                            self.space.remove(
                                self.t, self.t1, self.t2, self.t3)
                            self.make_target
            # Vector dirandvel
            if n == 1:
                line = [ball_pos, pygame.mouse.get_pos()]
                pygame.draw.line(self.screen, (255, 0, 0), line[0], line[1], 3)
            self.space.debug_draw(draw_options)
            pygame.display.update()
            # only run once user launches/clicks second time
            if update:
                # rolling friction / for whatever reason, if allowed to apply in the air it will dampen way too much.
                if self.body.position[1] > 696:
                    self.ball.body.angular_velocity *= 0.975
                self.space.step(0.001)
                if (self.pos_g[0] - 50) < (self.body.position)[0] < (self.pos_g[0] + 50) and (self.pos_g[1] - 40) < self.body.position[1] < (self.pos_g[1] + 40) and winable:
                    print("You win! \nGo again if you like.")
                    winable = False
                    won = True

    def place_ball(self, ball_pos):
        """places ball at given click position"""
        self.body = pymunk.Body(mass=1, moment=10)
        self.body.position = (ball_pos)
        self.ball = pymunk.Circle(self.body, radius=20)
        self.ball.elasticity = 0.5
        self.ball.friction = 0.75
        self.space.add(self.body, self.ball)

    def set_dirandvel(self, pos):
        """should draw arrow to click and wait """
        p0 = self.body.position
        x, y = pos
        p1 = Vec2d(x=float(x), y=float(y))
        impulse = 5 * (p1 - p0)
        self.body.apply_impulse_at_local_point(impulse)

    def reset(self):
        """removes previous ball"""
        self.space.remove(self.body)
        self.space.remove(self.ball)

    def make_target(self):
        gsz = 60/2
        t_x = random.randint(100, 1180)
        t_y = random.randint(100, 620)
        self.pos_g = (t_x, t_y)
        self.t = pymunk.Body(mass=1, moment=10)
        print(self.pos_g)
        self.t.position = (self.pos_g)
        self.t1 = pymunk.Segment(self.space.static_body,
                                 (t_x - gsz, t_y - gsz), (t_x - gsz, t_y + gsz), 2)
        self.t1.elasticity = 0.99999
        self.t1.friction = 0.999
        self.t2 = pymunk.Segment(self.space.static_body,
                                 (t_x - gsz, t_y + gsz), (t_x + gsz, t_y + gsz), 2)
        self.t2.elasticity = 0.99999
        self.t2.friction = 0.999
        self.t3 = pymunk.Segment(self.space.static_body,
                                 (t_x + gsz, t_y - gsz), (t_x + gsz, t_y + gsz), 2)
        self.t3.elasticity = 0.99999
        self.t3.friction = 0.999
        self.space.add(self.t, self.t1, self.t2, self.t3)


if __name__ == "__main__":
    main()
