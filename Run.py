from Init import init_main

def run_main():
	init_main()
	# late import because of variable initialization
	from Game.OnEvents import on_game_step

	while 1:
		on_game_step()

run_main()

