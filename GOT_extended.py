import pymunk
import pymunk.pygame_util
import pygame
import random

import pymunk.shapes
from pymunk.vec2d import Vec2d


def main():
    print("This is GOT. Two Players, random target, better rules. \nYou place the ball, set its launch direction and initial speed as well as reset by left clicking. \
            \nThere are Trickshots (bounces [+1 point for each] and scoring from below the target [3 points]) and a randomized wind, displayed with the gravity in the top left. \nGot it? Let's go.")
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
        wind = random.randint(-500, 500)
        self.space.gravity = (wind, 981)
        # make world boundaries
        for i in range(4):
            segment = pymunk.Segment(
                self.space.static_body, pts[i], pts[(i+1) % 4], 4)
            segment.elasticity = 0.75
            segment.friction = 0.75
            segment.collision_type = 1
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
        # players
        self.current_Player = 1
        # track
        self.score = [0, 0]
        self.collisions = 0
        self.from_below = False

    def run(self):
        """Well. It runs the game."""
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        # loop flags / one could do without them and just use n, but for the sake of readabillity, flags
        n = 0
        update = False
        winable = False
        run = True
        won = False
        yeetable = True
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
                        if (self.pos_g[0] - 40) < (ball_pos)[0] < (self.pos_g[0] + 35) and (self.pos_g[1] - 40) < ball_pos[1] < (self.pos_g[1] + 40):
                            print(
                                "Yea. Right. Nice try. You get skipped. It's the other Players turn now.")
                            if self.current_Player == 1:
                                self.current_Player = 2
                            else:
                                self.current_Player = 1
                        elif ball_pos[1] < self.pos_g[1]:
                            print(
                                "You need to place the ball below the target or this isn't much fun.")
                        else:
                            self.place_ball(ball_pos)
                            winable = True
                            n += 1
                    elif n == 1:
                        self.set_dirandvel(ball_pos)
                        if abs(self.body.velocity[0]) > 5000 or abs(self.body.velocity[1]) > 2500 and yeetable:
                            print("Achievement unlocked: YEET!")
                            yeetable = False
                        n += 1
                        update = True
                    elif n == 2:
                        self.reset()
                        update = False
                        n = 0
                        if won:
                            # new target
                            self.space.remove(
                                self.t, self.t1, self.t2, self.t3)
                            self.make_target()
                            won = False
                            # new wind
                            wind = random.randint(-500, 500)
                            self.space.gravity = (wind, 981)
            # gravity and wind display
            pygame.draw.line(self.screen, (155, 100, 100),
                             (80, 10), (80, 108), 3)
            wind = self.space.gravity[0]/10
            pygame.draw.line(self.screen, (0, 0, 255),
                             (80, 10), (80 + wind, 10), 3)
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
                # win check
                if (self.pos_g[0] - 20) < (self.body.position)[0] < (self.pos_g[0] + 20) and (self.pos_g[1] - 20) < self.body.position[1] < (self.pos_g[1] + 20) and winable:
                    # how many points
                    worth = 1 + self.collisions + self.from_below*4
                    self.score[self.current_Player-1] += worth
                    if worth == 1:
                        print("Point for Player" + str(self.current_Player) +
                              "!\nScore is: " + str(self.score))
                    else:
                        print(str(worth) + " Points for Player" + str(self.current_Player) +
                              "!\nScore is: " + str(self.score))
                    if self.score[0] > 20 or self.score[1] > 20:
                        print(
                            "\n\n Hey. You've been playing quite a bit. I'm glad you like the game.\n\n")
                    if self.score[0] > 100 or self.score[1] > 100:
                        print("Go touch some grass.")

                    winable = False
                    won = True
                # collision detection
                handler = self.space.add_collision_handler(1, 2)
                handler.begin = self.collide

    def collide(self, arbiter, space, data):
        self.collisions += 1
        return True

    def place_ball(self, ball_pos):
        """places ball at given click position"""
        self.body = pymunk.Body(mass=1, moment=10)
        self.body.position = (ball_pos)
        self.ball = pymunk.Circle(self.body, radius=20)
        self.ball.elasticity = 0.5
        self.ball.friction = 0.75
        self.ball.collision_type = 2
        self.space.add(self.body, self.ball)
        if (self.pos_g[0] - 50) < (self.body.position)[0] < (self.pos_g[0] + 50) and self.pos_g[1] < self.body.position[1]:
            self.from_below = True

    def set_dirandvel(self, pos):
        """should draw arrow to click"""
        p0 = self.body.position
        x, y = pos
        p1 = Vec2d(x=float(x), y=float(y))
        impulse = 5 * (p1 - p0)
        self.body.apply_impulse_at_local_point(impulse)

    def reset(self):
        """removes previous ball"""
        self.space.remove(self.body)
        self.space.remove(self.ball)
        self.collisions = 0
        self.from_below = False
        if self.current_Player == 1:
            self.current_Player = 2
        else:
            self.current_Player = 1

    def make_target(self):
        gsz = 60/2
        t_x = random.randint(100, 1180)
        t_y = random.randint(100, 620)
        self.pos_g = (t_x, t_y)
        self.t = pymunk.Body(mass=1, moment=10)
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
        self.all_t = (self.t, self.t1, self.t2, self.t3)
        self.space.add(self.t, self.t1, self.t2, self.t3)


if __name__ == "__main__":
    main()
