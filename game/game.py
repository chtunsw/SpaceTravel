import pygame
from pathlib import Path
from enum import Enum
from random import randrange

GAME_NAME = "Space Travel"
WIN_WIDTH, WIN_HEIGHT = 450, 800
STAR_MIN_RADIUS = 2
STAR_MAX_RADIUS = 5
TRANSPARENT_COLOR = (0, 0, 0, 0)
SPACE_BLUE = (10, 25, 50)
STAR_WHITE = (255, 255, 255)
SCORE_FONT_FAMILY = "comicsans"
SCORE_FONT_SIZE = 24
SCORE_FONT_COLOR = (10, 200, 130)
IMGS_DIR = Path(__file__).parent.absolute() / "imgs"
SPACESHIP_IMG = pygame.image.load((IMGS_DIR / "spaceship.png").as_posix())


class Direction(Enum):

    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class Star(pygame.sprite.Sprite):

    def __init__(self, x, y, radius):
        super().__init__()
        self.radius = radius
        self.transparent_color = TRANSPARENT_COLOR
        self.color = STAR_WHITE
        self.image = pygame.Surface([2 * self.radius, 2 * self.radius])
        self.image.fill(self.transparent_color)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.tick_count = 0
        self.velocity = 0.5
        self.acceleration = 0.001
    
    def update(self):
        center_x, center_y = self.rect.center
        self.tick_count += 1
        displacement = self.velocity * self.tick_count + 0.5 * self.acceleration * self.tick_count ** 2
        new_center_y = int(center_y + displacement)
        self.rect.center = (center_x, new_center_y)


class SpaceShip(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = SPACESHIP_IMG
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 15
    
    def move(self, direction, display_surf):
        x_max, y_max = display_surf.get_size()
        new_center_x, new_center_y = center_x, center_y = self.rect.center
        displacement = self.velocity
        if direction == Direction.UP:
            expected_y = int(center_y - displacement)
            new_center_y = expected_y if expected_y > 0 else 0
        elif direction == Direction.DOWN:
            expected_y = int(center_y + displacement)
            new_center_y= expected_y if expected_y < y_max else y_max
        elif direction == Direction.LEFT:
            expected_x = int(center_x - displacement)
            new_center_x = expected_x if expected_x > 0 else 0
        elif direction == Direction.RIGHT:
            expected_x = int(center_x + displacement)
            new_center_x = expected_x if expected_x < x_max else x_max
        self.rect.center = (new_center_x, new_center_y)
    
    def render(self, display_surf):
        display_surf.blit(self.image, self.rect.topleft)


class App:

    def __init__(self):
        self.name = GAME_NAME
        self.is_running = False
        self.score = 0
        self.score_font_family = SCORE_FONT_FAMILY
        self.score_font_size = SCORE_FONT_SIZE
        self.score_font_color = SCORE_FONT_COLOR
        self.display_surf = None
        self.size = self.width, self.height = WIN_WIDTH, WIN_HEIGHT
        self.space_blue = SPACE_BLUE
        self.spaceship = None
        self.star_min_radius = STAR_MIN_RADIUS
        self.star_max_radius = STAR_MAX_RADIUS
        self.star_list = pygame.sprite.Group([])

    def init_game(self):
        pygame.init()
        pygame.display.set_caption(self.name)
        self.spaceship = SpaceShip(int(self.width / 2), int(self.height / 3 * 2))
        self.display_surf = pygame.display.set_mode(self.size)
        self.is_running = True
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False
    
    def udpate_state(self):
        self.update_stars()
        self.handle_spaceship_move()
        self.collision_detect()
        self.increase_score_with_clock()

    def update_screen(self):
        self.display_surf.fill(self.space_blue)
        self.star_list.draw(self.display_surf)
        self.spaceship.render(self.display_surf)
        self.render_score()
        pygame.display.update()

    def run(self):
        self.init_game()
        clock = pygame.time.Clock()
        while (self.is_running):
            for event in pygame.event.get():
                self.handle_event(event)
            self.udpate_state()
            self.update_screen()
            clock.tick(30)
        self.stop()

    def stop(self):
        pygame.quit()

    def update_stars(self):
        new_star = Star(randrange(0, self.width), 0, randrange(self.star_min_radius, self.star_max_radius))
        self.star_list.add(new_star)
        self.star_list.update()
        for star in self.star_list.sprites():
            if star.rect.center[1] > self.height:
                self.star_list.remove(star)

    def handle_spaceship_move(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.spaceship.move(Direction.UP, self.display_surf)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.spaceship.move(Direction.DOWN, self.display_surf)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.spaceship.move(Direction.LEFT, self.display_surf)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.spaceship.move(Direction.RIGHT, self.display_surf)
    
    def collision_detect(self):
        if pygame.sprite.spritecollide(self.spaceship, self.star_list, False):
            self.is_running = False
    
    def increase_score_with_clock(self):
        self.score += 1

    def render_score(self):
        score_string = "Score: {}".format(self.score)
        score_font = pygame.font.SysFont(self.score_font_family, self.score_font_size)
        current_score = score_font.render(score_string, 1, self.score_font_color)
        self.display_surf.blit(current_score, (8, 8))


if __name__ == "__main__":
    app = App()
    app.run()