import Init
from Game.Low import V2
import Game.GmObjects as Objects

#
window_size = Init.window_size
b_count_xy = Init.b_count_xy
b_size_xy = Init.b_size_xy

#
Player = Init.Player
Camera = Init.Camera
game_map = Init.game_map

#
vo_update_required = False

#
save_visible_objects: list = []
save_camera_pos = V2(0, 0)


def get_near_objects(check_pos, cmap_pixels: dict, radius=1):
	fine_list = []

	cx, cy = check_pos
	key: tuple
	for key in cmap_pixels.keys():
		kx, ky = V2(key)
		dx, dy = abs(cx - kx), abs(cy - ky)
		if dx <= radius and dy <= radius:
			fine_list.extend(cmap_pixels[key])

	return fine_list


def create_object_pixelmap(object_list, block_div=1):
	# determine best output format
	# todo: Indexing as quick check, if 'PixelCollision' then BoxCheck, so on...
	# todo: check collisions for all near-pixel objects? (for objs bigger than one sqare)

	unique = ['block', ]
	object_map = {}

	obj: Objects.GameObject
	for obj in object_list:
		index = obj.pos.to_tuple()

		# create key if not already present
		if index not in object_map.keys():
			object_map[index] = []

		# skip unique objects
		if obj.tname in unique:
			if any([t_obj.tname == obj.tname for t_obj in object_map[index]]):
				continue

		object_map[index].append(obj)

	return object_map


def update_vo_list(game_map: Objects.GameMap, camera_pos, b_count_xy):
	print("VO update")

	visible_objects = []
	b_size_xy = game_map.b_size_xy

	gm_object: Objects.GameObject
	for gm_object in game_map.map_objects:
		obj_beg = gm_object.pos * b_size_xy
		obj_beg_x, obj_beg_y = obj_beg
		obj_end_x, obj_end_y = obj_beg + b_size_xy

		bounds_beg = b_size_xy * camera_pos
		bounds_size = b_size_xy * b_count_xy

		scr_beg_x, scr_beg_y = bounds_beg
		scr_end_x, scr_end_y = bounds_beg + bounds_size

		inside_screen = obj_end_x >= scr_beg_x and obj_beg_x < scr_end_x
		inside_screen &= obj_end_y >= scr_beg_y and obj_beg_y < scr_end_y

		if inside_screen:
			visible_objects.append(gm_object)

	game_map.update_vo_list_from(visible_objects)


def filter_pixelmap_single(cmap_pixels):
	collision_map = {}
	key: tuple
	for key in cmap_pixels:
		n_obj = len(cmap_pixels[key])
		if n_obj > 1:
			collision_map[key] = cmap_pixels[key]

	return collision_map
