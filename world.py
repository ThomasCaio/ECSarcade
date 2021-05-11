import esper
from components import unit
from components import render


class MainWorld(esper.World):
    def __int__(self, *args, **kwargs):
        super(MainWorld, self).__init__(*args, **kwargs)

    def create_player(self, name):
        self.create_entity(unit.Unit(name), unit.Player(), render.Renderable(), render.Velocity())

    def create_monster(self, name):
        self.create_entity(unit.Unit(name), unit.Enemy(), render.Renderable(), render.Velocity())

    def event_handler(self, event):
        ...
