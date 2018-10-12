import Init
from Game.Low import V2

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


def require_visual_update():
	global vo_update_required
	vo_update_required = True


def update_vo_list(camera_pos):
	global save_visible_objects, game_map, b_size_xy, b_count_xy

	save_visible_objects.clear()

	for gm_object in game_map.map_objects:
		obj_beg = gm_object.pos * b_size_xy
		obj_beg_x, obj_beg_y = obj_beg
		obj_end_x, obj_end_y = obj_beg + b_size_xy

		bounds_beg = b_size_xy * camera_pos
		bounds_size = b_size_xy * b_count_xy

		scr_beg_x, scr_beg_y = bounds_beg
		scr_end_x, scr_end_y  = bounds_beg + bounds_size

		inside_screen = obj_end_x >= scr_beg_x and obj_beg_x < scr_end_x
		inside_screen &= obj_end_y >= scr_beg_y and obj_beg_y < scr_end_y

		if inside_screen:
			save_visible_objects.append(gm_object)


def get_vo_list() -> list:
	global vo_update_required
	global save_visible_objects
	global save_camera_pos

	if Camera.pos.NEQ(save_camera_pos, tolerance=0.5) or vo_update_required:
		save_camera_pos = V2(*Camera.pos)
		update_vo_list(Camera.pos)
		vo_update_required = False

	return save_visible_objects[:]


def handle_single_collision(Player, Other):
	if not Player.name == 'player': raise ValueError("Fuck off")

	if Other.name == 'block':
		oend = V2(Init.game_map.block_size, Init.game_map.block_size)

	if Other.name == 'apple':
		Other._to_destroy = True


def process_collisions(collision_list):

	for x in collision_list:
		if 'player' == x.name:
			others = collision_list[:]
			others.remove(x)
			print("Player in collision with: ", others)
			for other in others:
				handle_single_collision(x, other)


def create_finecheck_map(cmap_pixels: dict, center, radius=1):
	fine_list = []

	cx, cy = center
	for key in cmap_pixels.keys():
		kx, ky = V2(key)
		dx, dy = abs(cx - kx), abs(cy - ky)
		if dx <= 1 and dy <= 1:
			fine_list.append(cmap_pixels[key])

	return fine_list


def create_cmap_pixels(object_list, block_div=1):
	# determine best output format
	# todo: Indexing as quick check, if 'PixelCollision' then BoxCheck, so on...
	# todo: check collisions for all near-pixel objects? (for objs bigger than one sqare)

	unique = ['block', ]
	object_map = {}

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


def get_cmap_collisions(object_list, block_div=1):
	cmap_pixels = create_cmap_pixels(object_list, block_div)
	collision_map = {}
	for key in cmap_pixels:
		n_obj = len(cmap_pixels[key])
		if n_obj > 1:
			collision_map[key] = cmap_pixels[key]

	return collision_map
