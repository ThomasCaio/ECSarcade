from esper import Processor
from arcade import check_for_collision_with_list, SpriteList
from components.render import Renderable, Velocity
from components.unit import Player, Monster, Name
import math


class MovementProcessor(Processor):
    def process(self):
        from components.render import Velocity, Renderable, Block
        blocked_tiles = SpriteList()
        [blocked_tiles.append(x[1][0]) for x in self.world.get_components(Renderable, Block)]
        for ent, (vel, rend, name) in self.world.get_components(Velocity, Renderable, Name):
            rend.center_x += vel.x
            if check_for_collision_with_list(rend, blocked_tiles):
                rend.center_x += (vel.x * -1)
            rend.center_y += vel.y
            if check_for_collision_with_list(rend, blocked_tiles):
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


class AnimationProcessor(Processor):
    def process(self, *args, **kwargs):
        from components.render import Renderable
        for ent, (rend) in self.world.get_components(Renderable):
            print(ent)
            rend[0].update_animation()


class ProjectileProcessor(Processor):
    def process(self, *args, **kwargs):
        from components.projectile import Projectile
        for ent, (proj, vel) in self.world.get_components(Projectile, Velocity):
            proj.center_x += vel.x
            proj.center_y += vel.y


class MonsterAI(Processor):
    def process(self, *args, **kwargs):
        for m, (render, monster, vel) in self.world.get_components(Renderable, Monster, Velocity):
            self.find_player(render, monster)
            if monster.target:
                dist = calculate_distance(render, self.world.component_for_entity(monster.target, Renderable))
                if 1000 >= dist >= 120:
                    self.follow_target(render, monster, vel)
                else:
                    vel.x = 0
                    vel.y = 0

    def find_player(self, render, monster):
        for p, (player, _player) in self.world.get_components(Renderable, Player):
            dist = calculate_distance(render, player)
            if 1000 >= dist >= 80:
                monster.target = p

    def follow_target(self, render, monster, velocity):
        target = self.world.component_for_entity(monster.target, Renderable)
        if render.center_y < target.center_y:
            velocity.y = min(velocity.speed, target.center_y - render.center_y)
        elif render.center_y > target.center_y:
            velocity.y = min(velocity.speed, render.center_y - target.center_y) *(-1)

        if render.center_x < target.center_x:
            velocity.x = min(velocity.speed, target.center_x - render.center_x)
        elif render.center_x > target.center_x:
            velocity.x = min(velocity.speed, render.center_x - target.center_x) * (-1)


def calculate_distance(monster, player):
    return math.sqrt((player.center_x - monster.center_x)**2 + (player.center_y - monster.center_y) ** 2)


class InputProcessor(Processor):
    def process(self, *args, **kwargs):
        ...
