import pygame
import Init
from Game import Objects, Get

#
clock = pygame.time.Clock()
BACK_COLOR = (0, 0, 0)

#
Camera = Init.Camera
Player = Init.Player
images = Init.images
game_map = Init.game_map

#
window_size = Init.window_size
block_size = game_map.block_size

#
screen = pygame.display.set_mode(window_size)


def QuickText(Text):
	font = pygame.font.SysFont('Calibri', 15, 0, 0)
	txtRender = font.render(Text, 0, (0x77,0x77,0x77))
	return txtRender


def DrawGameObjects():
	global visible_objs
	global lcp

	visible_objs = Get.get_vo_list()
	draw_objs = [Player]
	draw_objs.extend(visible_objs)

	for go in draw_objs:

		image = images[go.tname]
		dx, dy = (go.pos - Camera.pos) * block_size
		screen.blit(image, (dx, dy, 0, 0))

	pos_label = QuickText("Player X,Y: {:.2f},{:.2f}".format(*Player.pos))
	screen.blit(pos_label, (0,0,0,0))


def graphics_step():
	screen.fill(BACK_COLOR)
	DrawGameObjects()
	pygame.display.flip()

	clock.tick(60)