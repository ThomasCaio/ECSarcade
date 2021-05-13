from arcade import Sprite, load_texture, color, Texture, draw_rectangle_outline, draw_polygon_outline
import PIL

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


class Velocity:
    def __init__(self, x=0.0, y=0.0, speed=1):
        self.x = x
        self.y = y
        self.speed = speed


class Block:
    def __init__(self):
        ...


class Renderable(Sprite):
    def __init__(self, static=True, *args, **kwargs):
        if kwargs.get('filename'):
            self.filename = kwargs['filename']
        super(Renderable, self).__init__(hit_box_algorithm='None', *args, **kwargs)
        self.static = static
        self.idle = True
        self.walking_textures = {UP: [], LEFT: [], DOWN: [], RIGHT: []}
        self.direction = UP

        self.hover = False
        self.target = False

        if not static:
            self.load_spritesheet()

    def on_draw(self):
        if self.hover and not self.target:
            draw_polygon_outline(self.points, color.WHITE)
            return
        elif self.target and not self.hover:
            draw_polygon_outline(self.points, color.RED)
            return
        elif self.target and self.hover:
            draw_polygon_outline(self.points, color.ORIOLES_ORANGE)

    def load_spritesheet(self):
        for i in range(8):
            self.walking_textures[UP].append(load_texture(self.filename, x=(i * 64), y=8 * 64, width=64, height=64))
        for i in range(8):
            self.walking_textures[LEFT].append(load_texture(self.filename, x=(i * 64), y=9 * 64, width=64, height=64))
        for i in range(8):
            self.walking_textures[DOWN].append(load_texture(self.filename, x=(i * 64), y=10 * 64, width=64, height=64))
        for i in range(8):
            self.walking_textures[RIGHT].append(load_texture(self.filename, x=(i * 64), y=11 * 64, width=64, height=64))

        self.texture = self.walking_textures[UP][0]
        points = ((-19.0, -19.0), (-12.0, -30.0), (12.0, -30.0), (17.0, -19.0),
                  (17.0, 7.0), (12.0, 19.0), (-12.0, 19.0), (-19.0, 7.0))
        self.set_hit_box(points)

    def update_animation(self, delta_time: float = 1 / 60):
        if not self.static and not self.idle:
            self.cur_texture_index += 1
            if self.cur_texture_index > 7 * 10:
                self.cur_texture_index = 0
            frame = self.cur_texture_index // 10
            self.texture = self.walking_textures[self.direction][frame]


def create_rectangle_outline(width, height, color, opacity, line):
    img = PIL.Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(img)
    draw.rectangle(((0, 0), (width, height)), outline=(*color, opacity), width=line)
    name = f"outlinedsquare:{width}x{height}:{color}"
    return Texture(name, img)
