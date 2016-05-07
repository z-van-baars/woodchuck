import pygame
import assets
import objects
import game_map


class SelectionBox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = assets.white
        self.image = pygame.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.start_pos = None
        self.draw_box = False

    def resize(self, pos):
        if pos[0] >= self.start_pos[0] and pos[1] >= self.start_pos[1]:
            self.image = pygame.Surface([pos[0] - self.start_pos[0], pos[1] - self.start_pos[1]])
            self.rect.x = self.start_pos[0]
            self.rect.y = self.start_pos[1]

        elif pos[0] >= self.start_pos[0] and pos[1] < self.start_pos[1]:
            self.image = pygame.Surface([pos[0] - self.start_pos[0], self.start_pos[1] - pos[1]])
            self.rect.x = self.start_pos[0]
            self.rect.y = pos[1]

        elif pos[0] < self.start_pos[0] and pos[1] >= self.start_pos[1]:
            self.image = pygame.Surface([self.start_pos[0] - pos[0], pos[1] - self.start_pos[1]])
            self.rect.x = pos[0]
            self.rect.y = self.start_pos[1]

        elif pos[0] < self.start_pos[0] and pos[1] < self.start_pos[1]:
            self.image = pygame.Surface([self.start_pos[0] - pos[0], self.start_pos[1] - pos[1]])
            self.rect.x = pos[0]
            self.rect.y = pos[1]

        self.image.fill(assets.white)


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("Woodchuck")
    screen_width = 1920
    screen_height = 1080  
    screen = pygame.display.set_mode([screen_width, screen_height], pygame.FULLSCREEN)
    ui_pane = pygame.image.load("art/ui_pane.png").convert()
    ui_pane.set_colorkey(assets.key)
    clock = pygame.time.Clock()
    time = 0
    font = pygame.font.SysFont('Calibri', 25, True, False)

    map_1 = game_map.GameMap()
    maps = [map_1]
    current_map = 0
    maps[current_map].wood = 200

    done = False
    selection_box = SelectionBox()
    ui_elements = pygame.sprite.Group()
    ui_elements.add(selection_box)
    selected = pygame.sprite.Group()
    action = None

    while not done:
        pos = pygame.mouse.get_pos()

        mouse_coord_stamp = font.render(str(pos), False, assets.black)
        wood_count_stamp = font.render(str(maps[current_map].wood), False, assets.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_which_mouse_button = pygame.mouse.get_pressed()
                if check_which_mouse_button[0]:
                    if 1846 <= pos[0] <= 1899 and 9 <= pos[1] <= 47:
                        done = True
                    elif 20 <= pos[0] <= 1900 and 63 <= pos[1] <= 854:
                        # if something is selected
                        if len(selected) > 0:
                            selected = pygame.sprite.Group()

                        else:
                            if not selection_box.draw_box:
                                selection_box.draw_box = True
                                selection_box.start_pos = pos
                                selection_box.rect.x = pos[0]
                                selection_box.rect.y = pos[1]
                elif check_which_mouse_button[1]:
                    if len(selected) > 0:
                        for unit in selected:
                            unit.target = pos


            elif event.type == pygame.MOUSEBUTTONUP:
                if selection_box.draw_box:
                    selection_box.draw_box = False
                    selection_box.start_pos = None
                    selection_box.rect.x = 0
                    selection_box.rect.y = 0
                    selection_box.image = pygame.Surface([1, 1])
                    selection_box.image.fill(assets.white)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    pass

        maps[current_map].update()
        screen.blit(maps[current_map].background_image, [20, 63])
        screen.blit(ui_pane, [0, 0])
        screen.blit(mouse_coord_stamp, [1700, 15])
        screen.blit(wood_count_stamp, [70, 17])
        if selection_box.draw_box:
            selection_box.resize(pos)
            ui_elements.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        time += 1


if __name__ == "__main__":
    main()