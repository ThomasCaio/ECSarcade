# import win32con
# import win32gui

# the_program_to_hide = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

import arcade
from components.point import Point, point_collision
from world import MainWorld
from components.render import *
from components.unit import *
import processors
import timeit


world = MainWorld()
world.add_processor(processors.MovementProcessor())
world.add_processor(processors.AnimationProcessor())
world.add_processor(processors.MonsterAI())

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

VIEWPORT_MARGIN_X = (SCREEN_WIDTH // 2) - 16
VIEWPORT_MARGIN_Y = (SCREEN_HEIGHT // 2) - 16

SCREEN_TITLE = "Starting Template"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.center_window()

        self.all_sprites = None
        self.hover = None

        self.up_pressed = False
        self.left_pressed = False
        self.down_pressed = False
        self.right_pressed = False

        self.player = None

        self.mouse = (0, 0)
        self.mouse_pos = (0, 0)

        self.view_left = 0
        self.view_bottom = 0

        self.zoom = 0
        self.min_zoom = -600
        self.max_zoom = 600

        self.frame_count = 0
        self.fps = 0
        self.fps_start_timer = None

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.all_sprites = arcade.SpriteList()

        self.player = world.create_entity(Player(),
                                          Velocity(speed=2),
                                          Renderable(static=False, filename='resources/human_warrior.png', center_x=100,
                                                     center_y=100),
                                          Name('Demnok'), Block())

        for i in range(10):
            world.create_entity(Monster(), Velocity(), Renderable(static=False, filename='resources/human_warrior.png', center_x=150, center_y=50+(i*60)),
                                Name(f'Monster #{i}'), Block())

        self.all_sprites.extend([x for ent, [x] in world.get_components(Renderable)])

    def on_draw(self):
        fps_calculation_freq = 60
        if self.frame_count % fps_calculation_freq == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = fps_calculation_freq / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1

        arcade.start_render()

        for ent, (rend, name) in world.get_components(Renderable, Name):
            rend.draw()
            rend.on_draw()
            arcade.draw_text(name.name, rend.center_x-32, rend.center_y-50, arcade.color.WHITE)
            # rend.draw_hit_box()

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, self.view_left+20, self.view_bottom+20, arcade.color.BLACK, 18)
            arcade.draw_text(f"Sprites: {len(world.get_component(Renderable))}", self.view_left+20, self.view_bottom+60, arcade.color.BLACK, 18)
        arcade.finish_render()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        x += dx
        y += dy
        self.mouse = (x, y)
        prop_x = x / SCREEN_WIDTH
        prop_y = y / SCREEN_HEIGHT
        mouse_x = self.get_viewport()[0] + ((SCREEN_WIDTH + self.zoom) * prop_x)
        mouse_y = self.get_viewport()[2] + ((SCREEN_HEIGHT + (self.zoom * 0.75)) * prop_y)

        self.mouse_pos = Point(mouse_x, mouse_y)
        for ent, (rend, monster, name) in world.get_components(Renderable, Monster, Name):
            if point_collision(self.mouse_pos, rend):
                rend.hover = True
                break
            rend.hover = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == 4:
            for ent, (rend, monster, name) in world.get_components(Renderable, Monster, Name):
                if point_collision(self.mouse_pos, rend):
                    rend.target = not rend.target
                    break
        elif button == 1:
            player = world.component_for_entity(self.player, Renderable)
            monsters = arcade.SpriteList()
            names = []
            [monsters.append(x[1][0]) for x in world.get_components(Renderable, Monster, Name)]
            [names.append(x[1][2]) for x in world.get_components(Renderable, Monster, Name)]
            for m in monsters:
                print(arcade.get_distance_between_sprites(player, m), names[monsters.index(m)])

            # mon, dist = arcade.get_closest_sprite(player, monsters)
            # print(mon, dist, names[monsters.index(mon)])

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.up_pressed = True
        if symbol == arcade.key.A:
            self.left_pressed = True
        if symbol == arcade.key.S:
            self.down_pressed = True
        if symbol == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.up_pressed = False
        if symbol == arcade.key.A:
            self.left_pressed = False
        if symbol == arcade.key.S:
            self.down_pressed = False
        if symbol == arcade.key.D:
            self.right_pressed = False

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        scroll_y *= -30
        if not (scroll_y >= 0 and self.zoom >= self.max_zoom) and not (scroll_y <= 0 and self.zoom <= self.min_zoom):
            self.zoom += scroll_y

    def _update_camera(self, player):
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN_X + (self.zoom//2)
        if player.left < left_boundary:
            self.view_left -= left_boundary - player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN_X + (self.zoom//2)
        if player.right > right_boundary:
            self.view_left += player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_Y + ((self.zoom*0.75)//2)
        if player.top > top_boundary:
            self.view_bottom += player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN_Y + ((self.zoom*0.75)//2)
        if player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - player.bottom
            changed = True

        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            left = self.view_left
            right = SCREEN_WIDTH + self.view_left + self.zoom
            bottom = self.view_bottom

            # 0.75 means 4:3 screen proportion
            top = SCREEN_HEIGHT + self.view_bottom + (self.zoom*0.75)
            arcade.set_viewport(left,
                                right,
                                bottom,
                                top)

    def on_update(self, delta_time):
        self.on_mouse_motion(*self.mouse, 0, 0)

        vel = world.component_for_entity(self.player, Velocity)
        rend = world.component_for_entity(self.player, Renderable)
        self._update_camera(rend)

        vel.x, vel.y = 0, 0
        if self.up_pressed and not self.down_pressed:
            vel.y = vel.speed
            rend.direction = 0
        elif self.down_pressed and not self.up_pressed:
            vel.y = -vel.speed
            rend.direction = 2
        if self.left_pressed and not self.right_pressed:
            vel.x = -vel.speed
            rend.direction = 1
        elif self.right_pressed and not self.left_pressed:
            vel.x = vel.speed
            rend.direction = 3

        # if vel.x == 0 and vel.y == 0:
            # rend.idle = True
            # rend.texture = rend.walking_textures[rend.direction][0]
        # else:
            # rend.idle = False

        world.process()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
