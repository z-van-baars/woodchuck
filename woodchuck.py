import pygame
import assets
import objects
import game_map
import math


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

    def resize(self, pos, screen_width, screen_height):
        self.x = pos[0] - self.start_pos[0]
        self.y = pos[1] - self.start_pos[1]

        if pos[0] < 21:
            self.x = 21 - self.start_pos[0]
        elif pos[0] > screen_width - 20:
            self.x = (screen_width - 20) - self.start_pos[0]
        if pos[1] < 63:
            self.y = 63 - self.start_pos[1]
        elif pos[1] > screen_height - 224:
            self.y = (screen_height - 224) - self.start_pos[1]

        new_box = pygame.Rect(self.start_pos[0], self.start_pos[1], self.x, self.y)

        return new_box

    def draw_box(self, screen_width, screen_height, pos):
        if 20 <= pos[0] <= (screen_width - 20) and 63 <= pos[1] <= (screen_height - 226):
            if not self.box_active:
                self.box_active = True
                self.start_pos = pos
            else:
                self.box_image = self.resize(pos, screen_width, screen_height)

    def close_box(self, current_map, pos, screen_dims):
        selected = []
        if self.box_active:
            self.box_image = self.resize(pos, screen_dims[0], screen_dims[1])
            for unit in current_map.units:
                if self.box_image.colliderect(unit):
                    selected.append(unit)
            if len(selected) == 0:
                for building in current_map.buildings:
                    if self.box_image.colliderect(building):
                        selected.append(building)
        print("turning off the box now")
        self.box_active = False
        self.start_pos = (0, 0)
        return selected


def close_game_check(event, pos, screen_width, screen_height):
    close_box_left_bound = screen_width - 74
    close_box_right_bound = screen_width - 21
    close_box_top_bound = 9
    close_box_bottom_bound = 47
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed(0):
            if close_box_left_bound <= pos[0] <= close_box_right_bound and close_box_top_bound <= pos[1] <= close_box_bottom_bound:
                pygame.QUIT()


def none_selected(event, selection_box, current_map, pos, screen_dims):
    selected = []
    if event.type == pygame.MOUSEBUTTONDOWN:
        check_which_mouse_button = pygame.mouse.get_pressed()
        if check_which_mouse_button[0]:
            close_game_check(event, pos, screen_dims[0], screen_dims[1])
            selection_box.draw_box(screen_dims[0], screen_dims[1], pos)
        elif check_which_mouse_button[1]:
            # Right click processing, probably nothing with nothing selected
            pass

    elif event.type == pygame.MOUSEBUTTONUP:
        if selection_box.box_active:
            selected = selection_box.close_box(current_map, pos, screen_dims)

    elif event.type == pygame.KEYDOWN:
        # keypress processing
        pass

    elif event.type == pygame.KEYUP:
        # key release processing
        pass
    return selected


def units_selected(event, selection_box, selected, current_map, pos, screen_dims):
    if event.type == pygame.MOUSEBUTTONDOWN:
        check_which_mouse_button = pygame.mouse.get_pressed()
        if check_which_mouse_button[0]:
            close_game_check(event, pos, screen_dims[0], screen_dims[1])
            selection_box.draw_box(screen_dims[0], screen_dims[1], pos)

        elif check_which_mouse_button[1]:
            # Right click processing
            pass

    elif event.type == pygame.MOUSEBUTTONUP:
        check_which_mouse_button = pygame.mouse.get_pressed()
        if check_which_mouse_button[0]:
            selected = selection_box.close_box(current_map, pos, screen_dims)
        elif check_which_mouse_button[1]:
            # Right click release processing
            pass

    elif event.type == pygame.KEYDOWN:
        # keypress processing based on internal methods for unit selected
        pass

    elif event.type == pygame.KEYUP:
        # key release processing based on internal methods for unit selected
        pass

    return selected


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

    build_mode = False

    done = False
    selection_box = SelectionBox()
    selected = []

    ui_elements = pygame.sprite.Group()

    while not done:
        pos = pygame.mouse.get_pos()

        mouse_coord_stamp = font.render(str(pos), False, assets.black)
        wood_count_stamp = font.render(str(maps[current_map].wood), False, assets.white)
        build_mode_stamp = font.render("Build Mode", True, assets.black)
        lumber_camp_stamp = font.render("Lumber Camp", True, assets.black)
        serf_stamp = font.render("Serf", True, assets.black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if len(selected) == 0:
                selected = none_selected(event, selection_box, maps[current_map], pos, (screen_width, screen_height))

            else:
                selected = units_selected(event, selection_box, selected, maps[current_map], pos, (screen_width, screen_height))


        maps[current_map].update()
        screen.blit(maps[current_map].background_image, [20, 63])
        screen.blit(ui_pane, [0, 0])
        screen.blit(mouse_coord_stamp, [1700, 15])
        screen.blit(wood_count_stamp, [70, 17])
        if len(selected) > 0:
            for each in selected:
                name = each.name
            selected_stamp = font.render(name, True, assets.black)
            screen.blit(selected_stamp, [200, 870])

        if build_mode:
            building_cursor.rect.x = pos[0]
            building_cursor.rect.y = pos[1]
            for each in ui_elements:
                each.valid_build_site()
            ui_elements.draw(screen)
            screen.blit(build_mode_stamp, [200, 870])

        maps[current_map].buildings.draw(screen)

        if selection_box.box_active:
            box = selection_box.resize(pos, screen_width, screen_height)
            pygame.draw.rect(screen, assets.white, box, 1)
        pygame.display.flip()
        clock.tick(60)
        time += 1


if __name__ == "__main__":
    main()