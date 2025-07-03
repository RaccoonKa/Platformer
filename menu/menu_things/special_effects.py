import pygame

# Coffee
class CoffeeEffect:
    def __init__(self, GAME_WIDTH, GAME_HEIGHT):
        self.images = [
            pygame.image.load("assets(menu)/pictures/secrets/coffee/0.png").convert_alpha(),
            pygame.image.load("assets(menu)/pictures/secrets/coffee/1.png").convert_alpha(),
            pygame.image.load("assets(menu)/pictures/secrets/coffee/2.png").convert_alpha()
        ]
        self.original_images = [img.copy() for img in self.images]
        self.current_index = -1
        self.position = (GAME_WIDTH // 6.25, GAME_HEIGHT // 1.36)
        self.active = False
        self.scale = 1.0

    # Resize
    def resize_images(self, scale):
        self.scale = scale
        for i, original_img in enumerate(self.original_images):
            if original_img:
                new_width = int(original_img.get_width() * scale)
                new_height = int(original_img.get_height() * scale)
                self.images[i] = pygame.transform.scale(original_img, (new_width, new_height))

    # Switch images
    def next_image(self):
        self.current_index += 1
        if self.current_index >= len(self.images):
            self.current_index = -1
            self.active = False
        else:
            self.active = True

    # Draw
    def draw(self, surface):
        if self.active and 0 <= self.current_index < len(self.images):
            img = self.images[self.current_index]
            x = self.position[0] - img.get_width() // 2
            y = self.position[1] - img.get_height() // 2
            surface.blit(img, (x, y))
