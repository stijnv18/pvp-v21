import pygame
import sys
import time

# TODO: if sys.platform != "win32": sys.exit(-1)

# TODO: check return values voor errors
pygame.init()
pygame.display.init()

clock = pygame.time.Clock()

# TODO: delete garbage global variables
HEIGHT = 800
WIDTH = 800
HEIGHT_SCALED = 27 / 450 * HEIGHT
WIDTH_SCALED = 36 / 400 * WIDTH
HEALTHBAR_WIDTH_SCALED = 64 / 192 * WIDTH * 0.7
HEALTHBAR_HEIGHT_SCALED = 9 / 192 * HEIGHT * 0.7

PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = 0.12

surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
pygame.display.set_icon(pygame.image.load(r"./images/icon.png"))

class Images:
	background = pygame.transform.scale(pygame.image.load(r"./images/background.png"), (WIDTH, HEIGHT))
	healthbar = pygame.transform.scale(pygame.image.load(r"./images/healthbar.png"), (HEALTHBAR_WIDTH_SCALED, HEALTHBAR_HEIGHT_SCALED))
	healthbar_flipped = pygame.transform.scale(pygame.transform.flip(healthbar, True, True), (HEALTHBAR_WIDTH_SCALED, HEALTHBAR_HEIGHT_SCALED))
	badhealth = pygame.image.load(r"./images/badhealth.png")
	badhealth_flipped = pygame.transform.flip(badhealth, True, True)
	countdown_3 = pygame.image.load(r"./images/countdown_3.png")
	countdown_2 = pygame.image.load(r"./images/countdown_2.png")
	countdown_1 = pygame.image.load(r"./images/countdown_1.png")
	countdown_1 = pygame.image.load(r"./images/countdown_1.png")
	player_1 = pygame.transform.scale(pygame.image.load(r"./images/player_1.png"), (WIDTH_SCALED, HEIGHT_SCALED))
	player_2 = pygame.transform.scale(pygame.image.load(r"./images/player_2.png"), (WIDTH_SCALED, HEIGHT_SCALED))

class Game:
	def __init__(self):
		self.entities = []
		self.player1 = Player(1)
		self.player2 = Player(2)
		self.entities += [self.player1, self.player2]
	# TODO: store all entities in here, this makes it easier to create a new game

class Entity:
	def __init__(self, image, position):
		self.image = image
		self.position = position
		self.velocity = pygame.math.Vector2(0, 0)
		self.acceleration = pygame.math.Vector2(0, 0)

	def draw(self):
		surface.blit(self.image, self.position)

	def update(self):
		pass

class Player(Entity):
	def __init__(self, id):
		self.id = id

		image = getattr(Images, f"player_{id}")
		image_width = image.get_width()
		image_height = image.get_height()
		pos = pygame.math.Vector2(((WIDTH - image_width) // 2, (35 if id == 2 else HEIGHT - image_height - 35)))
		super().__init__(image, pos)

	def update(self):
		self.acceleration.x += self.velocity.x * -PLAYER_FRICTION
		self.velocity += self.acceleration
		self.position += self.velocity + PLAYER_ACCELERATION * self.acceleration
		
		if self.position.x > WIDTH - self.image.get_width() - WIDTH_SCALED // 2 - 5:
			self.position.x = WIDTH - self.image.get_width() - WIDTH_SCALED // 2 - 5
		if self.position.x < WIDTH_SCALED // 2 + 5: 
			self.position.x = WIDTH_SCALED // 2 + 5
		
		self.acceleration = pygame.math.Vector2(0, 0)

	def move_left(self):
		self.acceleration.x = -PLAYER_ACCELERATION

	def move_right(self):
		self.acceleration.x = PLAYER_ACCELERATION

class Projectile(Entity):
	pass

game = Game()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# TODO: convert naar match-case
	pressed_keys = pygame.key.get_pressed()
	if (pressed_keys[pygame.K_q]):
		game.player1.move_left()
	if (pressed_keys[pygame.K_d]):
		game.player1.move_right()
	if (pressed_keys[pygame.K_RIGHT]):
		game.player2.move_left()
	if (pressed_keys[pygame.K_LEFT]):
		game.player2.move_right()

	surface.blit(Images.background, (0, 0))

	surface.blit(Images.healthbar_flipped, ((WIDTH - Images.healthbar_flipped.get_width()) // 2, 5))
	surface.blit(Images.healthbar, ((WIDTH - Images.healthbar.get_width()) // 2, HEIGHT - Images.healthbar.get_height() - 5))

	for entity in game.entities:
		entity.update()
		entity.draw()
	
	pygame.display.update()
	surface.fill((255, 255, 255))
	clock.tick(60)

pygame.display.quit()
pygame.quit()

sys.exit(0)