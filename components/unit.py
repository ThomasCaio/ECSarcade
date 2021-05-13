class Name:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Unit:
    def __init__(self):
        self.max_health = 100
        self.health = 100


class Monster:
    def __init__(self):
        self.target = None


class Player:
    def __init__(self):
        ...
