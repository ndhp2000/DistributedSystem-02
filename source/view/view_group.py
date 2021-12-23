import pygame
from source.view.player import PlayerView
from source.config import *

class ViewGroup:
    def __init__(self, model_group, view_class_init_function): # View class init
        super().__init__()
        self._view_class_init_function = view_class_init_function
        self._model_group = model_group

    def draw(self, screen: pygame.Surface):
        for entity in self._model_group:
            if entity.is_removed():
                continue
            view_entity = self._view_class_init_function(entity)
            view_entity.add_to_parent(screen, view_entity.get_world_position(), is_centered=True)


class PlayerViewGroup(ViewGroup):
    def __init__(self, model_group, view_class_init_function=PlayerView):
        super().__init__(model_group, view_class_init_function)

        self._view_entities = {}
        self._name_tags = {}

        self._name_tag_font_ = pygame.font.SysFont('notomono', PLAYER_TAG_FONT_SIZE)

        for entity in self._model_group:
            self._view_entities[entity.get_id()] = view_class_init_function(entity)
            self._name_tags[entity.get_id()] = self._name_tag_font_.render(f'P{entity.get_id()}', True, (255, 255, 255))

    def draw(self, screen):
        lost_entities = self._model_group.get_removed_entities()
        if len(lost_entities) != 0:
            for entity in lost_entities:
                del self._view_entities[entity.get_id()]
                del self._name_tags[entity.get_id()]

        if len(self._model_group) > len(self._view_entities):
            self._view_entities = {}
            for entity in self._model_group:
                self._view_entities[entity.get_id()] = self._view_class_init_function(entity)
                self._name_tags[entity.get_id()] = self._name_tag_font_.render(
                    f'P{entity.get_id()}', True, (255, 255, 255))

        for entity_id in self._view_entities:
            view_entity = self._view_entities[entity_id]
            view_entity.add_to_parent(screen, view_entity.get_world_position(), is_centered=True)

            name_tag = self._name_tags[entity_id]
            position = view_entity.get_world_position()
            screen.blit(name_tag, (position[0] - 5, position[1] + 10))