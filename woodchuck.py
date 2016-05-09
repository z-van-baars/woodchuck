import pygame
import assets
import objects
import game_map
import math


class VariableCase(object):
    def __init__(self):
        super().__init__()
        self.screen_width = 0
        self.screen_height = 0
        self.screen = None
        self.ui_pane = None
        self.clock = None
        self.time = 0
        self.font = None

        self.map_1 = game_map.GameMap()
        self.maps = [self.map_1]
        self.current_map = 0
        self.maps[self.current_map].wood = 200

        self.build_mode = False

        self.done = False
        self.selection_box = None
        self.selected = []

        self.unit_to_place = None

        self.ui_elements = None

game_globals = VariableCase()


class SelectionBox(object):
    def __init__(self):
        super().__init__()
        self.start_pos = (0, 0)
        self.box_active = False
        self.x = 0
        self.y = 0
        self.end_pos = None
        self.width = 1
        self.box_image = pygame.Rect(self.start_pos[0], self.start_pos[1], self.x, self.y)

    def resize(self):
        self.x = game_globals.pos[0] - self.start_pos[0]
        self.y = game_globals.pos[1] - self.start_pos[1]

        if game_globals.pos[0] < 21:
            self.x = 21 - self.start_pos[0]
        elif game_globals.pos[0] > game_globals.screen_width - 20:
            self.x = (game_globals.screen_width - 20) - self.start_pos[0]
        if game_globals.pos[1] < 63:
            self.y = 63 - self.start_pos[1]
        elif game_globals.pos[1] > game_globals.screen_height - 224:
            self.y = (game_globals.screen_height - 224) - self.start_pos[1]

        new_box = pygame.Rect(self.start_pos[0], self.start_pos[1], self.x, self.y)

        return new_box

    def draw_box(self):
        if 20 <= game_globals.pos[0] <= (game_globals.screen_width - 20) and 63 <= game_globals.pos[1] <= (game_globals.screen_height - 226):
            if not self.box_active:
                self.box_active = True
                self.start_pos = game_globals.pos
            else:
                self.box_image = self.resize()

    def close_box(self):
        if self.box_active:
            self.box_image = self.resize()
            for unit in game_globals.maps[game_globals.current_map].units:
                if self.box_image.colliderect(unit):
                    game_globals.selected.append(unit)
            if len(game_globals.selected) == 0:
                for building in game_globals.maps[game_globals.current_map].buildings:
                    if self.box_image.colliderect(building):
                        game_globals.selected.append(building)
        self.box_active = False
        self.start_pos = (0, 0)


def close_game_check(event):
    close_box_left_bound = game_globals.screen_width - 74
    close_box_right_bound = game_globals.screen_width - 21
    close_box_top_bound = 9
    close_box_bottom_bound = 47
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed(0):
            if close_box_left_bound <= game_globals.pos[0] <= close_box_right_bound and close_box_top_bound <= game_globals.pos[1] <= close_box_bottom_bound:
                pygame.QUIT()


def event_dispatcher():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_globals.done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                check_which_mouse_button = pygame.mouse.get_pressed()
                if check_which_mouse_button[0]:
                    close_game_check(event)
                    game_globals.selection_box.draw_box()
                elif check_which_mouse_button[1]:
                    # Right click processing, probably nothing with nothing selected
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:
                if game_globals.selection_box.box_active:
                    game_globals.selection_box.close_box()

            elif event.type == pygame.KEYDOWN:
                if build_mode:
                    game_globals.unit_to_place = build_mode(event)

                elif event.key == pygame.K_b:
                    game_globals.build_mode = True

            elif event.type == pygame.KEYUP:
                # key release processing
                pass


def build_mode(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        check_which_mouse_button = pygame.mouse.get_pressed()
        if check_which_mouse_button[0]:
            x = game_globals.pos[0]
            y = game_globals.pos[1]
            current_map = game_globals.maps[game_globals.current_map]
            new_unit = objects.unit_to_place(x, y, current_map)
            current_map.units.add(new_unit)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            unit = objects.serf
    return unit


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("Woodchuck")

    game_globals.screen_width = 1920
    game_globals.screen_height = 1080
    game_globals.screen = pygame.display.set_mode([game_globals.screen_width, game_globals.screen_height], pygame.FULLSCREEN)
    game_globals.ui_pane = pygame.image.load("art/ui_pane.png").convert()
    game_globals.ui_pane.set_colorkey(assets.key)
    game_globals.clock = pygame.time.Clock()
    game_globals.time = 0
    game_globals.font = pygame.font.SysFont('Calibri', 25, True, False)

    game_globals.selection_box = SelectionBox()
    game_globals.ui_elements = pygame.sprite.Group()

    font = game_globals.font

    while not game_globals.done:
        game_globals.pos = pygame.mouse.get_pos()

        mouse_coord_stamp = font.render(str(game_globals.pos), False, assets.black)
        wood_count_stamp = font.render(str((game_globals.maps[game_globals.current_map]).wood), False, assets.white)
        build_mode_stamp = font.render("Build Mode", True, assets.black)
        lumber_camp_stamp = font.render("Lumber Camp", True, assets.black)
        serf_stamp = font.render("Serf", True, assets.black)

        event_dispatcher()

        game_globals.screen.blit(game_globals.maps[game_globals.current_map].background_image, [20, 63])
        game_globals.screen.blit(game_globals.ui_pane, [0, 0])
        game_globals.screen.blit(mouse_coord_stamp, [1700, 15])
        game_globals.screen.blit(wood_count_stamp, [70, 17])
        if len(game_globals.selected) > 0:
            selected_stamp = font.render(game_globals.selected[0].name, True, assets.black)
            game_globals.screen.blit(selected_stamp, [200, 870])

        game_globals.maps[game_globals.current_map].buildings.draw(game_globals.screen)

        if game_globals.selection_box.box_active:
            box = game_globals.selection_box.resize()
            pygame.draw.rect(game_globals.screen, assets.white, box, 1)
        pygame.display.flip()
        game_globals.clock.tick(60)
        game_globals.time += 1


if __name__ == "__main__":
    main()
