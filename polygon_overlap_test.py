import pygame
import sys

x = (1, 2)
y = (3, 4)

print()

pygame.init()
pygame.display.init()

WIDTH, HEIGHT, FPS = 500, 500, 60

clock = pygame.time.Clock()
surface = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_polygon(color, position, points):
	positioned_point = tuple(map(lambda point: tuple(map(lambda a, b: a + b, point, position)), points))
	pygame.draw.polygon(surface, color, positioned_point, 1)

def do_polygon_overlap(p1p, p1b, p2p, p2b):
	p1 = tuple(map(lambda p: tuple(map(lambda a, b: a + b, p, p1p)), p1b))
	p2 = tuple(map(lambda p: tuple(map(lambda a, b: a + b, p, p2p)), p2b))

	def is_point_in_polygon(point, polygon):
		point

	p1x = tuple(map(lambda a: a[0], p1)) # idk doesn't work when not converted to tuple
	p1minx = min(p1x)
	p1maxx = max(p1x)
	p2x = tuple(map(lambda a: a[0], p2)) # idk doesn't work when not converted to tuple
	p2minx = min(p2x)
	p2maxx = max(p2x)
	p1y = tuple(map(lambda a: a[1], p1)) # idk doesn't work when not converted to tuple
	p1miny = min(p1y)
	p1maxy = max(p1y)
	p2y = tuple(map(lambda a: a[1], p2)) # idk doesn't work when not converted to tuple
	p2miny = min(p2y)
	p2maxy = max(p2y)

	for i in range(p1minx, p2maxx):
		print(i)

	return True

running = True
while running:
	for event in pygame.event.get():
		match event.type:
			case pygame.QUIT:
				running = False

	p1p = (200, 200)
	p1b = ((0, 0), (0, 150), (150, 100), (100, -50))
	p1c = (0, 0, 255)

	p2p = pygame.mouse.get_pos()
	p2b = ((0, 0), (0, 75), (100, 100), (75, 0))
	p2c = (0, 255, 0) if do_polygon_overlap(p1p, p1b, p2p, p2b) else (255, 0, 0)

	draw_polygon(p1c, p1p, p1b)
	draw_polygon(p2c, p2p, p2b)

	pygame.display.update()
	surface.fill((0, 0, 0))
	deltatime = clock.tick(FPS)

pygame.display.quit()
pygame.quit()

sys.exit(0)