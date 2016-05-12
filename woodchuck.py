import pygame
import assets
import objects
import game_map
import math
import serf
import lumber_camp
import tree
import entity


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

        self.build_cursor = None

        self.ui_elements = None
        self.health_boxes_to_draw = None

game_globals = VariableCase()


class Stamps(object):
    def __init__(self):
        super().__init__()
        self.wood_count_stamp = None
        self.mouse_coord_stamp = None
        self.build_mode_stamp = None
        self.lumber_camp_stamp = None
        self.serf_stamp = None

    def update_live_stamps(self):
        font = game_globals.font

        self.to_build_stamp = None
        self.mouse_coord_stamp = font.render(str(game_globals.pos), False, assets.black)
        self.wood_count_stamp = font.render(str((game_globals.maps[game_globals.current_map]).wood), False, assets.white)

    def create_one_time_stamps(self):
        font = game_globals.font

        self.build_mode_stamp = font.render("Build Mode   (debug only - press 'e' to exit)", True, assets.black)
        self.lumber_camp_stamp = font.render("Lumber Camp", True, assets.black)
        self.serf_stamp = font.render("Serf", True, assets.black)


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

        # old buggy selection box code
        # self.x = game_globals.pos[0] - self.start_pos[0]
        # self.y = game_globals.pos[1] - self.start_pos[1]
        # self.x = abs(self.x)
        # self.y = abs(self.y)

        # if game_globals.pos[0] < 21:
            # self.x = 21 - self.start_pos[0]
        # elif game_globals.pos[0] > game_globals.screen_width - 20:
            # self.x = (game_globals.screen_width - 20) - self.start_pos[0]
        # if game_globals.pos[1] < 63:
            # self.y = 63 - self.start_pos[1]
        # elif game_globals.pos[1] > game_globals.screen_height - 224:
            # self.y = (game_globals.screen_height - 224) - self.start_pos[1]

        self.x = game_globals.pos[0] - self.start_pos[0]
        self.y = game_globals.pos[1] - self.start_pos[1]
        top_left_corner = self.start_pos
        if self.x < 0:
            self.x = abs(self.x)
            top_left_corner = (top_left_corner[0] - self.x, top_left_corner[1])
        if self.y < 0:
            self.y = abs(self.y)
            top_left_corner = (top_left_corner[0], top_left_corner[1] - self.y)

        new_box = pygame.Rect(top_left_corner[0], top_left_corner[1], self.x, self.y)

        return new_box

    def draw_box(self):
        if 20 <= game_globals.pos[0] <= (game_globals.screen_width - 20) and 63 <= game_globals.pos[1] <= (game_globals.screen_height - 226):
            if game_globals.build_mode:
                game_globals.build_mode = False
            if game_globals.selected:
                game_globals.selected = []
                game_globals.health_boxes_to_draw = pygame.sprite.Group()
            if not self.box_active:
                self.box_active = True
                self.start_pos = game_globals.pos
            else:
                self.box_image = self.resize()

    def close_box(self):
        if self.box_active:
            self.box_image = self.resize()
            for unit in game_globals.maps[game_globals.current_map].units:
                if self.box_image.colliderect(unit.rect):
                    game_globals.selected.append(unit)
                    game_globals.health_boxes_to_draw.add(unit.health_box)
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
                    if game_globals.build_mode:
                        debug_unit_selection(event)
                    game_globals.selection_box.draw_box()
                elif check_which_mouse_button[2]:
                    unit_at_target = None
                    target_grabber = pygame.Rect(game_globals.pos[0], game_globals.pos[1], 1, 1)
                    if len(game_globals.selected) > 0:
                        for unit in game_globals.maps[game_globals.current_map].units:
                            if target_grabber.colliderect(unit):
                                unit_at_target = unit
                        for each in game_globals.selected:
                            if unit_at_target:
                                each.target = unit_at_target
                                each.target_coords = (unit_at_target.rect.x, unit_at_target.rect.y)
                            else:
                                each.target_coords = (game_globals.pos[0], game_globals.pos[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                if game_globals.selection_box.box_active:
                    game_globals.selection_box.close_box()

            elif event.type == pygame.KEYDOWN:
                if game_globals.build_mode:
                    debug_unit_selection(event)

                elif event.key == pygame.K_b:
                    game_globals.build_mode = True

            elif event.type == pygame.KEYUP:
                # key release processing
                pass


def debug_unit_selection(event):

    if game_globals.unit_to_place != None:
        pygame.mouse.set_visible(0)
        if not game_globals.build_cursor:
            game_globals.build_cursor = game_globals.unit_to_place(game_globals.pos[0], game_globals.pos[1], game_globals.maps[game_globals.current_map])
        else:
            game_globals.build_cursor.rect.x = game_globals.pos[0]
            game_globals.build_cursor.rect.y = game_globals.pos[1]
        collisions_in_site = (pygame.sprite.spritecollide(game_globals.build_cursor, game_globals.maps[game_globals.current_map].units, False))
        if collisions_in_site:
            game_globals.build_cursor.image = game_globals.build_cursor.invalid_site_image
        else:
            game_globals.build_cursor.image = game_globals.build_cursor.build_image
        game_globals.ui_elements = pygame.sprite.Group()
        game_globals.ui_elements.add(game_globals.build_cursor)
    elif game_globals.unit_to_place == None:
        game_globals.build_cursor = None
        collisions_in_site = None

    if event.type == pygame.MOUSEBUTTONDOWN and game_globals.unit_to_place:
        check_which_mouse_button = pygame.mouse.get_pressed()
        if check_which_mouse_button[0]:
            if not collisions_in_site:
                pygame.mouse.set_visible(1)
                new_unit = game_globals.build_cursor
                new_unit.image = new_unit.built_image
                new_health_box = entity.HealthBox(new_unit.rect.x, new_unit.rect.y, new_unit.health, new_unit.max_health)
                new_unit_width = new_unit.image.get_width()
                new_health_box.get_new_position(new_unit.rect.x, new_unit.rect.y, new_unit_width)
                new_unit.health_box = new_health_box
                game_globals.unit_to_place = None
                game_globals.build_cursor = None
                game_globals.maps[game_globals.current_map].units.add(new_unit)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            game_globals.unit_to_place = serf.Serf
        elif event.key == pygame.K_l:
            game_globals.unit_to_place = lumber_camp.LumberCamp
        elif event.key == pygame.K_e:
            game_globals.build_mode = False
        elif event.key == pygame.K_t:
            game_globals.unit_to_place = tree.Tree


def render_screen_objects(render_stamps):
    game_globals.screen.blit(game_globals.maps[game_globals.current_map].background_image, [20, 63])
    game_globals.screen.blit(game_globals.ui_pane, [0, 0])
    game_globals.screen.blit(render_stamps.mouse_coord_stamp, [1700, 15])
    game_globals.screen.blit(render_stamps.wood_count_stamp, [70, 17])
    if len(game_globals.selected) > 0:
        for each in game_globals.selected:
            each.health_box.get_health_pixels(each.health)
            each_width = each.image.get_width()
            each.health_box.get_new_position(each.rect.x, each.rect.y, each_width)
        selected_stamp = game_globals.font.render(game_globals.selected[0].name, True, assets.black)
        game_globals.screen.blit(selected_stamp, [200, 870])

    game_globals.maps[game_globals.current_map].buildings.draw(game_globals.screen)
    game_globals.maps[game_globals.current_map].units.draw(game_globals.screen)
    game_globals.health_boxes_to_draw.draw(game_globals.screen)
    game_globals.ui_elements.draw(game_globals.screen)

    if game_globals.build_mode:
        game_globals.screen.blit(render_stamps.build_mode_stamp, [200, 870])

    if game_globals.selection_box.box_active:
        box = game_globals.selection_box.resize()
        pygame.draw.rect(game_globals.screen, assets.white, box, 1)


def init_game_state():
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
    game_globals.health_boxes_to_draw = pygame.sprite.Group()


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption("Woodchuck")

    init_game_state()

    render_stamps = Stamps()
    render_stamps.create_one_time_stamps()

    while not game_globals.done:
        game_globals.pos = pygame.mouse.get_pos()
        event_dispatcher()
        render_stamps.update_live_stamps()

        for each in game_globals.maps[game_globals.current_map].units:
            each.do_thing(game_globals.maps[game_globals.current_map])

        render_screen_objects(render_stamps)

        pygame.display.flip()
        game_globals.clock.tick(60)
        game_globals.time += 1


if __name__ == "__main__":
    main()
