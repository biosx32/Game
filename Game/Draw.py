import pygame
import Init
from Game import Get
import Game.GmObjects as Gmo

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
	txtRender = font.render(Text, 1, (0xA7,0xA7,0xA7))
	return txtRender


def DrawGameObjects():
	global visible_objs
	global lcp

	if Camera.pos.NEQ(lcp, tolerance=0.5):
		game_map.require_vo_update()
		lcp = Camera.pos

	draw_objs = game_map.get_vo_list()
	draw_objs.extend([Player])

	go: Gmo.GameObject
	for go in draw_objs:
		image = images[go.tname]
		dx, dy = (go.pos - Camera.pos) * block_size
		screen.blit(image, (dx, dy, 0, 0))

		go: Gmo.Player
		if go.tname == "player":
			a = QuickText("Energy {:1.2f}".format(go.jmp_energy))
			b = QuickText("Accel {:1.2f}".format(go.gaccel))
			screen.blit(a, (0, 30))
			screen.blit(b, (0, 60))


		if go.tname == "block":
			if not hasattr(go, 'label_cache'):
				go.label_cache = QuickText("{:3d}".format(go.gID))

			screen.blit(go.label_cache, ((go.pos - Camera.pos) * Init.b_size_xy).to_tuple())


		if go.in_collision:
			pygame.draw.rect(screen, (0, 255, 0), (dx, dy, *block_size), 2)

		if go.is_active():
			pygame.draw.rect(screen, (0, 255, 255), (dx, dy, *block_size), 2)
			pass

	pos_label = QuickText("Player X,Y: {:.2f},{:.2f}".format(*Player.pos))
	screen.blit(pos_label, (0,0,0,0))


def graphics_step():
	screen.fill(BACK_COLOR)
	DrawGameObjects()
	pygame.display.flip()

	clock.tick(60)