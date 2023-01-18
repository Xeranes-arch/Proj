import pymunk
import pymunk.pygame_util
import pygame
import random


def main():
    print("This is GOT. \nYou place the ball, set its launch direction and initial speed as well as reset by left clicking. \nGot it? Let's go. Press Enter to start:")
    # input()
    # init pygame with world ready to play
    world = World()
    world.run()


class World:

    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 981)
        size = (1080, 720)
        pts = [(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])]
        # make world boundaries
        for i in range(4):
            segment = pymunk.Segment(
                self.space.static_body, pts[i], pts[(i+1) % 4], 4)
            segment.elasticity = 0.999
            segment.friction = 0.999
            self.space.add(segment)
        # make target
        t1 = pymunk.Segment(self.space.static_body, (720, 720), (720, 320), 2)
        t1.elasticity = 0.99999
        t2 = pymunk.Segment(self.space.static_body, (770, 720), (770, 320), 2)
        t2.elasticity = 0.99999
        self.space.add(t1, t2)
        self.screen = pygame.display.set_mode(size)

    def run(self):
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        self.screen.fill((210, 210, 210))
        self.space.debug_draw(draw_options)
        pygame.display.update()

        run = True
        update = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                n = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if n == 0:
                        self.place_ball(pos)
                        n = n + 1
                    elif n == 1:
                        self.set_dirandvel(pos)
                        update = True
                    else:
                        self.reset()
                        update = False
                        n = 0
            if update:
                self.space.step(0.001)

            
    def simulate(self):
        self.space.step(0.001)

    def place_ball(self, pos):
        body = pymunk.Body(mass=1, moment=10)
        body.position = (pos)
        circle = pymunk.Circle(body, radius=30)
        circle.elasticity = 0.95
        self.space.add(body, circle)
        pass

    def set_dirandvel(self, pos):
        pass

    def reset(self):
        
        pass


if __name__ == "__main__":
    main()
