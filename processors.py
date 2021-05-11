from esper import Processor


class MovementProcessor(Processor):
    def process(self):
        from components.render import Velocity, Renderable
        for ent, (vel, rend) in self.world.get_components(Velocity, Renderable):
            rend.center_x += vel.x
            rend.center_y += vel.y


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
