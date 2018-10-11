import GameGraphics
import GameUpdate
import Init
import pygame
# ---------

Init.InitMain()
GameGraphics.GraphicsInit()

while 1:
	# --- Game logic
	GameUpdate.MainUpdate()

	# --- Drawing code

	GameGraphics.MainDraw()

