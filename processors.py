from esper import Processor
from arcade import check_for_collision_with_list, SpriteList, get_closest_sprite
from components.render import Renderable, Velocity
from components.unit import Player, Monster, Name
import math


class MovementProcessor(Processor):
    def __init__(self):
        self.blocked_tiles = SpriteList()

    def process(self):
        from components.render import Velocity, Renderable, Block
        [self.blocked_tiles.append(x[1][0]) for x in self.world.get_components(Renderable, Block)]
        for ent, (vel, rend, name) in self.world.get_components(Velocity, Renderable, Name):
            rend.center_x += vel.x
            if check_for_collision_with_list(rend, self.blocked_tiles):
                rend.center_x += (vel.x * -1)

            rend.center_y += vel.y
            if check_for_collision_with_list(rend, self.blocked_tiles):
                rend.center_y += (vel.y*-1)

            if not vel.x and not vel.y:
                rend.idle = True
                rend.texture = rend.walking_textures[rend.direction][0]
            else:
                rend.idle = False

            if vel.y > 0:
                rend.direction = 0
            elif vel.y < 0:
                rend.direction = 2
            if vel.x > 0:
                rend.direction = 3
            elif vel.x < 0:
                rend.direction = 1

            self.blocked_tiles.remove(rend)


class AnimationProcessor(Processor):
    def process(self, *args, **kwargs):
        from components.render import Renderable
        for ent, (rend) in self.world.get_components(Renderable):
            rend[0].update_animation()


class ProjectileProcessor(Processor):
    def process(self, *args, **kwargs):
        from components.projectile import Projectile
        for ent, (proj, vel) in self.world.get_components(Projectile, Velocity):
            proj.center_x += vel.x
            proj.center_y += vel.y


class MonsterAI(Processor):
    def __init__(self):
        self.targets = SpriteList()

    def process(self, *args, **kwargs):
        [self.targets.append(x[1][0]) for x in self.world.get_components(Renderable, Player)]
        for m, (render, monster, vel) in self.world.get_components(Renderable, Monster, Velocity):
            target, dist = get_closest_sprite(render, self.targets)
            if 1000 >= dist >= 120:
                self.follow_target(render, target, vel)
            else:
                vel.x = 0
                vel.y = 0

    def follow_target(self, monster, target, velocity):
        if monster.center_y < target.center_y:
            velocity.y = min(velocity.speed, target.center_y - monster.center_y)
        elif monster.center_y > target.center_y:
            velocity.y = min(velocity.speed, monster.center_y - target.center_y) *(-1)
        else:
            velocity.y = 0
        if monster.center_x < target.center_x:
            velocity.x = min(velocity.speed, target.center_x - monster.center_x)
        elif monster.center_x > target.center_x:
            velocity.x = min(velocity.speed, monster.center_x - target.center_x) * (-1)
        else:
            velocity.x = 0


def calculate_distance(monster, player):
    return math.sqrt((player.center_x - monster.center_x)**2 + (player.center_y - monster.center_y) ** 2)


class InputProcessor(Processor):
    def process(self, *args, **kwargs):
        ...
