import pygame


class AbstractGroup:
    def __init__(self):
        self._entities_dict = {}
        self._removed_entities = []

    def add(self, entity):
        self._entities_dict[entity] = 0

    def remove(self, entity):
        self._entities_dict[entity] = 1
        self._removed_entities.append(entity)

    def has(self, entity):
        if self._entities_dict[entity] == 1:
            return False
        return True

    def empty(self):
        for entity in self._entities_dict:
            self.remove(entity)
            entity.remove(self)

    def __len__(self):
        return len(list(self._entities_dict))


class Group(AbstractGroup):
    def __init__(self):
        super().__init__()

    def __iter__(self):
        return iter(list(self._entities_dict))

    def add(self, entity):
        super().add(entity)

    def update(self, *args, **kwargs):
        self._removed_entities = []

        for entity in self._entities_dict:
            if self.has(entity):
                entity.update(*args, **kwargs)

        for entity in self._removed_entities:
            del self._entities_dict[entity]


class ViewGroup:
    def __init__(self, model_group, view_class_init_function): #View class init
        super().__init__()
        self._view_class_init_function = view_class_init_function
        self._model_group = model_group

    def draw(self, screen: pygame.Surface):
        for entity in self._model_group:
            view_entity = self._view_class_init_function(entity)
            view_entity.add_to_parent(screen, view_entity.get_world_position(), is_centered=True)

