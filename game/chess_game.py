import sys, pygame, os

def draw_background():
    is_next_tile_dark = True
    for x in range(10):
        for y in range(10):
            if (is_next_tile_dark):
                screen.blit(dark_tile_64px,
                            (x * tile_side_length, y * tile_side_length))
            else:
                screen.blit(light_tile_64px,
                            (x * tile_side_length, y * tile_side_length))
            is_next_tile_dark = not is_next_tile_dark
        is_next_tile_dark = not is_next_tile_dark

current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
board_path = os.path.join(assets_path, 'board_elements')

# Initialize the pygame modules
pygame.init()

# Define constants and variables
tile_side_length = 64
screen_size = (tile_side_length * 10, tile_side_length * 10)

screen = pygame.display.set_mode(screen_size)

dark_tile = pygame.image.load(os.path.join(
    board_path, "brown_tile.png")).convert()
light_tile = pygame.image.load(os.path.join(
    board_path, "clay_tile.png")).convert()

dark_tile_64px = pygame.transform.scale(
    dark_tile, (tile_side_length, tile_side_length))
light_tile_64px = pygame.transform.scale(
    light_tile, (tile_side_length, tile_side_length))

draw_background()

pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
