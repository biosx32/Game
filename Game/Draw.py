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
b_count_xy = Init.b_count_xy

#
window_size = Init.window_size
block_size = game_map.b_size_xy

#
screen: pygame.SurfaceType = pygame.display.set_mode(window_size)
lcp = Init.Camera.pos

def QuickText(Text):
	font = pygame.font.SysFont('Calibri', 15, 0, 0)
	txtRender = font.render(Text, 0, (0x77,0x77,0x77))
	return txtRender


def DrawGameObjects():
	global visible_objs
	global lcp

	if Camera.pos.NEQ(lcp, tolerance=0.5):
		game_map.require_vo_update()
		lcp = Camera.pos

	draw_objs = game_map.get_vo_list()
	draw_objs.extend([Player])

	go: Objects.GameObject
	for go in draw_objs:
		image = images[go.tname]
		dx, dy = (go.pos - Camera.pos) * block_size
		screen.blit(image, (dx, dy, 0, 0))

		if go.is_active():
			pass
		if go.in_collision:
			pygame.draw.rect(screen, (0, 255, 0), (dx, dy, *block_size), 2)

	pos_label = QuickText("Player X,Y: {:.2f},{:.2f}".format(*Player.pos))
	screen.blit(pos_label, (0,0,0,0))


def graphics_step():
	screen.fill(BACK_COLOR)
	DrawGameObjects()
	pygame.display.flip()

	clock.tick(60)