import pygame
import sys
import GameUpdate
import Init
Player = Init.Player
Camera = Init.Camera


moveX = [0, 0]
moveY = [0, 0]
def ProcessKeyDU(event: pygame.event):
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












def OnPressEscape():
	pass
