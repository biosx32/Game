import pygame
from timeit import default_timer as timer
from Game.Draw import graphics_step
import Game.Get as Get
import Game.GmObjects as Gmo
import sys
from Game.Low import V2

import Init

Player = Init.Player
pos_save = Player.pos.copy()
Camera = Init.Camera
game_map = Init.game_map
moveX, moveY = [0, 0], [0, 0]
b_count_xy = Init.b_count_xy
b_size_xy = Init.b_size_xy
save_timer = timer()


def on_process_single_action(pobj: Gmo.GameObject, action: Gmo.Action):
	global old_pos
	return_actions = []

	act_name, arguments = action.unpack()
	print("Action", act_name, "triggered on:", str(pobj))

	if act_name == 'check_collision':
		pobj.in_collision = False

	if act_name == 'collision':
		pobj.in_collision = True
		return_actions.append(Gmo.Action("check_collision"))

	return return_actions


def on_process_actions(gmo: Gmo.GameObject):
	unprocessed = []
	actions_copy = gmo.get_actions()
	for action in actions_copy:

		return_actions = on_process_single_action(gmo, action)
		if return_actions:
			unprocessed.extend(return_actions)

	gmo.update_actions(unprocessed)

# add collision a
def on_object_collide(gmo_main: Gmo.GameObject, object_list: list):
	main_action = Gmo.Action("collision", data=object_list)
	side_action = Gmo.Action("collision", data=[gmo_main])

	gmo_main.add_action(main_action)

	gmo: Gmo.GameObject
	for gmo in object_list:
		gmo.add_action(side_action)


def get_near_objs_of(position, radius=1.0):
	check_list = game_map.get_vo_list()
	objects_map = Get.create_object_pixelmap(check_list, block_div=16)
	# clean_map = Get.filter_pixelmap_single(objects_map)
	near_objs = Get.get_near_objects(position, objects_map, radius=radius)

	return near_objs

def on_check_collisions():
	pl_coll = get_near_objs_of(Player.pos, radius=1)

	if pl_coll:
	#	on_object_collide(Player, pl_coll)
		pass


def player_on_ground():
	ghost_pos = V2(Player.pos.x , Player.pos.y + 0.1)
	ghost_pos_2 = V2(Player.pos.x, Player.pos.y - 0.1)

	og_gpl = bool(get_near_objs_of(ghost_pos, radius=1.1))
	og_gpl_top = bool(get_near_objs_of(ghost_pos_2, radius=1.1))

	og_pl = bool(get_near_objs_of(Player.pos, radius=1.1))

	return not og_gpl_top and (og_pl or og_gpl)

def on_player_move():
	global save_timer
	global moveX, moveY

	t_end = timer()

	GhostPlayer = Gmo.Player(Player.pos.copy())

	# move ghost player and check if he collides

	def UpdateRelative(relx, rely):
		GhostPlayer.pos = V2(Player.pos.x + relx, Player.pos.y + rely)
		if not get_near_objs_of(GhostPlayer.pos, radius=0.97):
			Player.pos = GhostPlayer.pos


	if player_on_ground():
		# reset forces
		Player.gaccel = 0
		Player.jmp_energy = 3

	else:
		# gravity
		if not moveY[0] or not Player.jmp_energy > 0:
			Player.gaccel += 0.01



	if moveY[0]:
		Player.jmp_energy -= 1

		if Player.jmp_energy > 0:
			Player.gaccel -= 0.07



	UpdateRelative(- moveX[0], 0)
	UpdateRelative(+ moveX[1], 0)
	UpdateRelative(0, + Player.gaccel)











	# save_timer = t_end

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

	obj: Gmo.GameObject
	for obj in visible_objs:
		if obj.is_active():
			on_process_actions(obj)

	on_process_actions(Player)


	# react on collisions and reset variables
	pass

def on_logic_step():
	on_check_events()
	on_update_vo_list()
	on_player_move()
	on_check_collisions()
	on_check_actions()



def on_game_step():
	try:
		on_logic_step()
		graphics_step()
	except pygame.error as e:
		msg = str(e)
		print(msg)
		pygame.quit()
		sys.exit(-1)
