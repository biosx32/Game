import pygame
import GameUpdate
import Init
import sys
import Tmp
import GameObjects

import TileLogic


from GameObjects import V2
BACK_COLOR = (0, 0, 0)
window_size = Init.window_size

Camera = Init.Camera
Player = Init.Player




images = Init.images
clock = pygame.time.Clock()
screen: pygame.SurfaceType = pygame.display.set_mode(window_size)

game_map = TileLogic.game_map

block_size = game_map.block_size
game_map.game_objects.append(Player)


def _init_rescale_images():
	for key in images.keys():
		images[key] = pygame.transform.scale(images[key], (block_size,block_size))

def GraphicsInit():
	_init_rescale_images()


def QuickText(Text):
	font = pygame.font.SysFont('Calibri', 15, 0, 0)
	txtRender = font.render(Text, 0, (0x77,0x77,0x77))
	return txtRender


def DrawGameObjects():
	global visible_objs
	global lcp

	visible_objs = GameUpdate.GetVisibleObjectBoolList()

	for i, go in enumerate(game_map.game_objects):
		if not visible_objs[i]:
			continue

		if go._to_destroy:
			if not go._draw_begun:
				go._draw_frames = 30
				go._draw_begun = True
			go._draw_frames -=1
			if go._draw_frames == 0:
				go._exploded = True
			image = images['explosion']
		else:
			image = images[go.name]


		pos = TileLogic.GetAbsPosition(go.pos - Camera.pos, block_size)
		box = *pos, 0,0
		screen.blit(image, box)


	pos_label = QuickText("Player X,Y: "+ str(Player.pos.ToIntegerTup()))
	screen.blit(pos_label, (0,0,0,0))


def MainDraw():
	screen.fill(BACK_COLOR)

	DrawGameObjects()
	pygame.display.flip()
	clock.tick(60)