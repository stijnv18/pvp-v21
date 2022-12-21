import pygame
pygame.init()

screen = pygame.display.set_mode([1280, 720])
bg = pygame.image.load('background.jpg')

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill((255, 255, 255))
	screen.blit(pygame.transform.smoothscale(bg,(screen.get_size())),(0,0))
	pygame.display.flip()
pygame.quit()