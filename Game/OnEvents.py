import pygame
from timeit import default_timer as timer
from Game.Draw import graphics_step
from Game.Get import get_vo_list, create_collision_map
import sys
import Init

Player = Init.Player
Camera = Init.Camera
moveX, moveY = [0, 0], [0, 0]

save_timer = timer()



def on_collision_check():
	check_list = get_vo_list()
	check_list.extend([Player])
	cmap = create_collision_map(check_list)
	for ckey in cmap:
		val = cmap[ckey]
		print(ckey, val)



def on_player_move():
	global save_timer
	global moveX, moveY

	t_end = timer()

	# if t_end - t_start > 0.2:
	if 1:
		Player.pos.x += (-moveX[0] + moveX[1])
		Player.pos.y += (-moveY[0] + moveY[1])

		save_timer = t_end

	# gravity
	#Player.pos.y += 0.01

	Player.pos = Player.pos.rectify()
	Player.pos = Player.pos.restrict(Init.game_map.size)

	Camera.pos = Player.pos - Init.b_count_xy / 2


def process_key(event: pygame.event):
	global moveX
	global moveY

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_w:
			moveY[0] = 0.2
		elif event.key == pygame.K_s:
			moveY[1] = 0.2
		elif event.key == pygame.K_a:
			moveX[0] = 0.2
		elif event.key == pygame.K_d:
			moveX[1] = 0.2

	if event.type == pygame.KEYUP:
		if event.key == pygame.K_w:
			moveY[0] = 0
		elif event.key == pygame.K_s:
			moveY[1] = 0
		elif event.key == pygame.K_a:
			moveX[0] = 0
		elif event.key == pygame.K_d:
			moveX[1] = 0


def on_check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

		elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			process_key(event)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			print("User pressed a mouse button")

		elif event.type == pygame.MOUSEMOTION:
			pass


def on_logic_step():
	on_check_events()
	# OnIteratePending()
	on_collision_check()
	on_player_move()


def on_game_step():
	try:
		on_logic_step()
		graphics_step()
	except pygame.error as e:
		msg = str(e)
		print(msg)
		pygame.quit()
		sys.exit(-1)
