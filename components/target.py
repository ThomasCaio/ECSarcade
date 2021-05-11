from arcade import Sprite, draw_rectangle_outline, color


class Target(Sprite):
    def __init__(self):
        super().__init__()
        self.hover = False
        self.target = False

    def on_draw(self, center_x, center_y, width, height):
        if self.hover:
            draw_rectangle_outline(center_x, center_y, width, height, color.WHITE, 1)
        if self.target:
            draw_rectangle_outline(center_x, center_y, width, height, color.RED, 1)
