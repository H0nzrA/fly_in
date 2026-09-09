import pygame
from ..domain import Zone, Connection


Window = pygame.surface.Surface
Clock = pygame.time.Clock
Event = pygame.event.Event
Surface = pygame.surface.Surface
Color = tuple[int, int, int, int]
Movement = Zone | Connection
