import pygame
import assets
import objects
import game_map


class SelectionBox(object):
    def __init__(self):
        super().__init__()
        self.color = assets.white
        self.start_pos = (0, 0)
        self.draw_box = False
        self.x = 0
        self.y = 0
        self.end_pos = None
        self.width = 1

    def resize(self, pos):
        self.x = pos[0] - self.start_pos[0]
        self.y = pos[1] - self.start_pos[1]
        new_box = pygame.Rect(self.start_pos[0], self.start_pos[1], self.x, self.y)

        return new_box


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
    selected = pygame.sprite.Group()

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
                        if not selection_box.draw_box:
                            selection_box.draw_box = True
                            selection_box.start_pos = pos

                elif check_which_mouse_button[1]:
                    if len(selected) > 0:
                        for unit in selected:
                            unit.target = pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if check_which_mouse_button[0]:

                    if selection_box.draw_box:
                        selection_box.draw_box = False
                        selection_box.start_pos = (0, 0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    pass

        maps[current_map].update()
        screen.blit(maps[current_map].background_image, [20, 63])
        screen.blit(ui_pane, [0, 0])
        screen.blit(mouse_coord_stamp, [1700, 15])
        screen.blit(wood_count_stamp, [70, 17])

        if selection_box.draw_box:
            box_image = selection_box.resize(pos)
            pygame.draw.rect(screen, assets.white, box_image, 1)
        pygame.display.flip()
        clock.tick(60)
        time += 1


if __name__ == "__main__":
    main()