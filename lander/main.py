import pygame
import sys

# TODO: if sys.platform != "win32": sys.exit(-1)

# TODO: check return values voor errors
pygame.init()
pygame.display.init()

clock = pygame.time.Clock()

# TODO: delete garbage global variables
WIDTH = 800
HEIGHT = 800
WIDTH_SCALED = 36 / 400 * WIDTH
HEIGHT_SCALED = 27 / 450 * HEIGHT
HEALTHBAR_WIDTH_SCALED = 64 / 192 * WIDTH * 0.7
HEALTHBAR_HEIGHT_SCALED = 9 / 192 * HEIGHT * 0.7
PROJECTILE_WIDTH_SCALED = 8 / 400 * WIDTH
PROJECTILE_HEIGHT_SCALED = 15 / 450 * HEIGHT
PROJECTILE_VELOCITY = 15

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
	player_1 = pygame.transform.scale(pygame.image.load(r"./images/player_1.png"), (WIDTH_SCALED, HEIGHT_SCALED))
	player_2 = pygame.transform.scale(pygame.image.load(r"./images/player_2.png"), (WIDTH_SCALED, HEIGHT_SCALED))
	projectile_1 = pygame.transform.scale(pygame.image.load(r"./images/projectile_1.png"), (PROJECTILE_WIDTH_SCALED, PROJECTILE_HEIGHT_SCALED))
	projectile_2 = pygame.transform.scale(pygame.image.load(r"./images/projectile_2.png"), (PROJECTILE_WIDTH_SCALED, PROJECTILE_HEIGHT_SCALED))

class Game:
	def __init__(self):
		self.player1 = Player(1)
		self.player2 = Player(2)
		self._entities = [self.player1, self.player2]

	def get_all_entities(self):
		return self._entities

	def get_all_entities_of_type(self, type):
		return [e for e in self._entities if e.type == type]

	def append_entity(self, entity):
		self._entities.append(entity)

	def delete_entity(self, entity):
		self._entities.remove(entity)

class Entity:
	class Type:
		PLAYER = 0
		PROJECTILE = 1

	def __init__(self, type, image, position, velocity=None, acceleration=None):
		self.type = type
		self.image = image
		self.position = position
		self.velocity = velocity if velocity is not None else pygame.math.Vector2(0, 0)
		self.acceleration = acceleration if acceleration is not None else pygame.math.Vector2(0, 0)

	def draw(self):
		surface.blit(self.image, self.position)

	def is_out_of_bounds(self, bounds):
		x1, y1, x2, y2 = bounds
		if not (x1 < self.position.x < x2 and y1 < self.position.y < y2):
			game.delete_entity(self)

	def update(self):
		pass

class Player(Entity):
	def __init__(self, id):
		self.id = id
		image = getattr(Images, f"player_{self.id}")
		position = pygame.math.Vector2(((WIDTH - image.get_width()) // 2, (35 if id == 2 else HEIGHT - image.get_height() - 35)))
		super().__init__(Entity.Type.PLAYER, image, position)

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

	def request_fire(self):
		position = self.position.copy()
		position.x += self.image.get_width() // 2
		velocity = pygame.math.Vector2(0, -PROJECTILE_VELOCITY if self.id == 1 else PROJECTILE_VELOCITY)
		projectile = Projectile(self.id, position, velocity)
		return projectile

class Projectile(Entity):
	def __init__(self, owner_id, position, velocity):
		self.owner_id = owner_id
		self.image = getattr(Images, f"projectile_{self.owner_id}")
		position.x -= self.image.get_width() // 2
		super().__init__(Entity.Type.PROJECTILE, self.image, position, velocity)

	def update(self):
		self.position += self.velocity

class Debug: # debugging shit
	enabled = True
	font = pygame.font.SysFont("arial.ttf", 24)
	_row_offset_y = 0

	def new_frame():
		Debug._row_offset_y = 0

	def draw_info(surface, text):
		fw, fh = Debug.font.size(text)
		surface.blit(Debug.font.render(text, True, (255, 0, 0)), (0, Debug._row_offset_y))
		Debug._row_offset_y += fh

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
	if (pressed_keys[pygame.K_z]):
		game.append_entity(game.player1.request_fire())
	if (pressed_keys[pygame.K_RIGHT]):
		game.player2.move_left()
	if (pressed_keys[pygame.K_LEFT]):
		game.player2.move_right()
	if (pressed_keys[pygame.K_UP]):
		game.append_entity(game.player2.request_fire())

	surface.blit(Images.background, (0, 0))

	surface.blit(Images.healthbar_flipped, ((WIDTH - Images.healthbar_flipped.get_width()) // 2, 5))
	surface.blit(Images.healthbar, ((WIDTH - Images.healthbar.get_width()) // 2, HEIGHT - Images.healthbar.get_height() - 5))

	for entity in game.get_all_entities():
		entity.update()
		entity.draw()
		if entity.is_out_of_bounds([0, 0, WIDTH, HEIGHT]):
			game.delete_entity(entity)

	if Debug.enabled: # debugging shit
		Debug.new_frame()
		Debug.draw_info(surface, f"Frames Per Second: {round(clock.get_fps())}")
		Debug.draw_info(surface, f"Frame Time (deltatime): {round(clock.get_time())}ms")
		Debug.draw_info(surface, f"Entity Count: {len(game._entities)}")
	
	pygame.display.update()
	surface.fill((255, 255, 255))
	deltatime = clock.tick(60)

pygame.display.quit()
pygame.quit()

sys.exit(0)