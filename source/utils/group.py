import pygame


class AbstractGroup:
    def __init__(self):
        self._entities_dict = {}

    def add(self, entity):
        self._entities_dict[entity] = 0

    def remove(self, entity):
        del self._entities_dict[entity]

    def empty(self):
        for entity in self._entities_dict:
            self.remove(entity)
            entity.remove(self)

    def __len__(self):
        return len(list(self._entities_dict))


class Group(AbstractGroup):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        for entity in self._entities_dict:
            entity.update(*args, **kwargs)


class ViewGroup(AbstractGroup):
    def __init__(self, model_group, class_init_function):
        super().__init__()

        for entity in model_group:
            entity_view = class_init_function(entity)
            self._entities_dict[entity_view] = 0

    def draw(self, screen: pygame.Surface):
        for entity_view in self._entities_dict:
            entity_view.add_to_parent(screen, entity_view.get_world_position())

