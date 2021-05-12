from esper import Processor
from arcade import check_for_collision_with_list, SpriteList


class MovementProcessor(Processor):
    def process(self):
        from components.render import Velocity, Renderable, Block
        blocked_tiles = SpriteList()
        [blocked_tiles.append(x[1][0]) for x in self.world.get_components(Renderable, Block)]
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            rend.center_x += vel.x
            if check_for_collision_with_list(rend, blocked_tiles):
                rend.center_x += (vel.x * -1)
            rend.center_y += vel.y
            if check_for_collision_with_list(rend, blocked_tiles):
                rend.center_y += (vel.y*-1)


class AnimationProcessor(Processor):
    def process(self, *args, **kwargs):
        from components.render import Renderable
        for ent, (rend) in self.world.get_components(Renderable):
            rend[0].update_animation()


class ProjectileProcessor(Processor):
    def process(self, *args, **kwargs):
        from components.projectile import Projectile
        from components.render import Velocity
        for ent, (proj, vel) in self.world.get_components(Projectile, Velocity):
            proj.center_x += vel.x
            proj.center_y += vel.y


class InputProcessor(Processor):
    def process(self, *args, **kwargs):
        ...
