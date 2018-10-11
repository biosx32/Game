import KeyEvent
import pygame
import Init
from timeit import default_timer as timer
from GameObjects import V2
import Tmp

Player = Init.Player
Camera = Init.Camera
window_size = Init.window_size
block_size = Init.blocks_vector

t_start = timer()

visible_objs = []
game_map = Init.game_map
lcp = V2(-1, -1)


if window_size[0]%block_size[0]!=0 or window_size[1]%block_size[0]!=0:
	Tmp.Errw("Block size not align or less")


def GetAbsPosition(Pos, b_size):
	x, y = Pos
	x = int(x * float(b_size))
	y = int(y * float(b_size))

	return V2(x, y)




urq = False
def RequireVisUpdate():
	global urq
	urq = True

def get_visible_objs(pos, block_count_v, game_map):
	visible_objects = []
	tile_size = V2(game_map.block_size, game_map.block_size)
	for go in game_map.game_objects:
		tile_beg_x, tile_beg_y = go.pos * tile_size

		bounds_size =  block_count_v * tile_size
		bounds_pos = pos * tile_size
		bounds_beg_x, bounds_beg_y = bounds_pos
		bounds_end_x, bounds_end_y  = bounds_pos + bounds_size

		if (tile_beg_x + tile_size.x >= bounds_beg_x and tile_beg_x < bounds_end_x) and \
			(tile_beg_y + tile_size.y  >= bounds_beg_y and tile_beg_y < bounds_end_y):
			visible_objects.append(1)
		else:
			visible_objects.append(0)



	return visible_objects

def GetVisibleObjectBoolList():
	global urq
	global visible_objs
	global lcp
	if Camera.pos.NEQ(lcp, tolerance=0.5) or urq:
		lcp = V2(*Camera.pos)
		visible_objs = get_visible_objs(Camera.pos, Init.blocks_vector, Init.game_map)
		urq = False
	return visible_objs

blocks = [0,0,0,0]

def HandleSingle(Player, Other):
	if not Player.name == 'player': raise ValueError("Fuck off")

	if Other.name == 'block':
		oend = V2(Init.game_map.block_size, Init.game_map.block_size)

	if Other.name == 'apple':
		Other._to_destroy = True

def HandleCollision(CollisionList):

	for x in CollisionList:
		if 'player' == x.name:
			others = CollisionList[:]
			others.remove(x)
			print("Player in collsion with: ", others)
			for other in others:
				HandleSingle(x, other)

def OnCollisionCheck():
	unique = ['block',]
	objects = GetVisibleObjectBoolList()
	vx, vy = Init.blocks_vector.ToIntegerTup()

	grid = [[[] for y in range(vy)] for x in range(vx)]

	for i, truth in enumerate(objects):
		if truth:
			obj = game_map.game_objects[i]
			px, py = (obj.pos - Camera.pos).ToMaximum(V2(vx,vy)).ToIntegerTup()
			if obj.name in unique:
				if any([x.name == obj.name for x in grid[px][py]]):
					continue

			grid[px][py].append(obj)

	for i in range(vx):
		for j in range(vy):
			current = grid[i][j]
			if len(current) > 1:
				HandleCollision(current)

def OnCheckEvents():

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
		elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			KeyEvent.ProcessKeyDU(event)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			print("User pressed a mouse button")

		elif event.type == pygame.MOUSEMOTION:
			pass

def OnIteratePending():
	update_list = []
	for object in game_map.game_objects:
		if not object._exploded:
			update_list.append(object)

	game_map.game_objects = update_list
	RequireVisUpdate()


def OnCalculate():
	global t_start
	moveX, moveY = KeyEvent.moveX, KeyEvent.moveY

	t_end = timer()

	#if t_end - t_start > 0.2:
	if 1:
		Player.pos.x += (-moveX[0]+moveX[1])
		Player.pos.y += (-moveY[0]+moveY[1])


		t_start = t_end

	Player.pos.y += 0.1

	Player.pos = Player.pos.ToAboveZero()
	Player.pos = Player.pos.ToMaximum(Init.map_size)


	Camera.pos = Player.pos - Init.blocks_vector/2

def MainUpdate():
	OnCheckEvents()
	OnIteratePending()
	OnCollisionCheck()
	OnCalculate()
