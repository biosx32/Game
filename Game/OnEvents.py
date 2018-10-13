import pygame
from timeit import default_timer as timer
from Game.Draw import graphics_step
import Game.Get as Get
import Game.Objects as Objects
import sys

import Init

Player = Init.Player
Camera = Init.Camera
game_map = Init.game_map
moveX, moveY = [0, 0], [0, 0]
b_count_xy = Init.b_count_xy

save_timer = timer()


def on_process_single_action(gmo: Objects.GameObject, action: Objects.Action):
	act_name, data = action.unpack()
	print("Action", act_name, "triggered on:", str(gmo))

	return_actions = []

	def add_action(action):
		return_actions.append(action)

	if gmo.tname == "player":
		if act_name == 'collision':
			other: Objects.GameObject
			for other in data:
				#game_map.delobject(other.gID)
				pass

	if gmo.tname == "block":

		if act_name == 'check_collision':
			gmo.in_collision = False

		if act_name == 'collision':
			gmo.in_collision = True
			add_action(Objects.Action("check_collision"))

	return return_actions


def on_process_actions(gmo: Objects.GameObject):
	unprocessed = []
	actions_copy = gmo.get_actions()
	for action in actions_copy:

		return_actions = on_process_single_action(gmo, action)
		if return_actions:
			unprocessed.extend(return_actions)

	gmo.update_actions(unprocessed)

# add collision a
def on_object_collide(gmo_main: Objects.GameObject, object_list: list):
	main_action = Objects.Action("collision", data=object_list)
	side_action = Objects.Action("collision", data=[gmo_main])

	gmo_main.add_action(main_action)

	gmo: Objects.GameObject
	for gmo in object_list:
		gmo.add_action(side_action)


def on_collision_check():
	#
	check_list = game_map.get_vo_list()
	coll_map = Get.create_cmap_pixels(check_list, block_div=4)
	clean_map = Get.get_cmap_collisions(coll_map)
	#
	pl_coll = Get.create_finecheck_map(coll_map, Player.pos, radius=1)

	if pl_coll:
		on_object_collide(Player, pl_coll)

	for key in clean_map:
		print("TODO collision: ", clean_map[key])

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


def on_update_vo_list():
	if game_map.vo_update_required:
		Get.update_vo_list(game_map, Camera.pos, b_count_xy)


def on_check_actions():
	visible_objs = game_map.get_vo_list()

	obj: Objects.GameObject
	for obj in visible_objs:
		if obj.is_active():
			on_process_actions(obj)

	on_process_actions(Player)


	# react on collisions and reset variables
	pass

def on_logic_step():
	on_check_events()
	on_update_vo_list()
	on_collision_check()
	on_check_actions()
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
