import pygame
import Game.GmObjects as Objects
import Game.Low as Low
from Game.Low import V2
from Game.GmObjects import GameMap
import os

if __name__ == "__main__":
	raise BlockingIOError("do not run this file lol...")

root_dir = os.getcwd() + "\\"

window_size = (1000, 700)
block_size = 50
b_count_xy = V2(window_size[0], window_size[1]) / block_size
b_size_xy = V2(block_size, block_size)

Camera = Objects.Camera()
Player = Objects.Player(V2(2, 2))
game_map = GameMap(root_dir + 'res\\map.bmp', b_size_xy)

images = {}




def init_load_images():
	global images
	images = {
		'block': pygame.image.load("res\\brick_block.png"),
		'player': pygame.image.load("res\\player2.png"),
		'explosion': pygame.image.load("res\\explosion.png")
	}

	_init_rescale_images()


def create_vars():
	init_load_images()



def check_vars():
	global window_size
	global b_size_xy
	result = window_size[0] % b_size_xy.x == 0 and \
			window_size[1] % b_size_xy.y == 0
	Low.assert_error(result, "Block size not align or less")


def _init_rescale_images():
	for key in images.keys():
		images[key] = pygame.transform.scale(images[key], (block_size,block_size))


def init_main():
	create_vars()
	check_vars()

	pygame.init()
	pygame.display.set_caption("Dumb/io")

