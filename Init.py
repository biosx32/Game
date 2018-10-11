import pygame
import GameObjects
from GameMap import GameMap
from GameObjects import V2
images = {}
window_size = (1000, 700)

Camera = GameObjects.Basic((0, 0), name="camera")
Player = GameObjects.Basic((2, 2), name="player")

block_size = 50
blocks_vector = GameObjects.V2 (window_size[0], window_size[1]) / block_size
game_map = GameMap('resrc\\map.bmp', block_size)
map_size = V2(*game_map.size)


def LoadImages():
	images['block'] = pygame.image.load("resrc\\brick_block.png")
	images['player'] = pygame.image.load("resrc\\player.png")
	images['explosion'] = pygame.image.load("resrc\\explosion.png")

def InitMain():
	# Initialize the game engine
	pygame.init()
	pygame.display.set_caption("Dumbio")

	LoadImages()

