import pymunk
import pymunk.pygame_util
import pygame

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
        self.screen = pygame.display.set_mode(size)
        # create space
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        # make world boundaries
        for i in range(4):
            segment = pymunk.Segment(
                self.space.static_body, pts[i], pts[(i+1) % 4], 4)
            segment.elasticity = 0.999
            segment.friction = 0.999
            self.space.add(segment)
        # make target
        t1 = pymunk.Segment(self.space.static_body,
                            (1020, 720), (1020, 320), 2)
        t1.elasticity = 0.99999
        t1.friction = 0.999
        t2 = pymunk.Segment(self.space.static_body,
                            (1070, 720), (1070, 320), 2)
        t2.elasticity = 0.99999
        t2.friction = 0.999
        self.space.add(t1, t2)
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
        # Interface starts running
        while run:
            self.screen.fill((210, 210, 210))
            # self.space.debug_draw(draw_options)
            # pygame.display.update()
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
            # Vector dirandvel
            if n == 1:
                line = [ball_pos, pygame.mouse.get_pos()]
                pygame.draw.line(self.screen, (255, 0, 0), line[0], line[1], 3)
            self.space.debug_draw(draw_options)
            pygame.display.update()
            # only run once user launches/clicks second time
            if update:
                self.space.step(0.001)
                if 1020 < (self.body.position)[0] < 1070 and self.body.position[1] > 696 and winable:
                    print("You win! \nGo again if you like.")
                    winable = False

    def place_ball(self, ball_pos):
        """places ball at given click position"""
        self.body = pymunk.Body(mass=1, moment=10)
        self.body.position = (ball_pos)
        self.ball = pymunk.Circle(self.body, radius=20)
        self.ball.elasticity = 0.2
        self.ball.friction = 0.5
        self.space.add(self.body, self.ball)

    def set_dirandvel(self, pos):
        """should draw arrow to click and wait """
        p0 = self.body.position
        x, y = pos
        p1 = Vec2d(x=float(x), y=float(y))
        impulse = 10 * (p1 - p0)
        self.body.apply_impulse_at_local_point(impulse)

    def reset(self):
        """removes previous ball"""
        self.space.remove(self.body)
        self.space.remove(self.ball)


if __name__ == "__main__":
    main()
