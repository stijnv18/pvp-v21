# TODO: use deltatime
# TODO: 

import pygame
import sys

# TODO: if sys.platform != "win32": sys.exit(-1)

# TODO: check return values voor errors
pygame.init()
pygame.display.init()

clock = pygame.time.Clock()

# TODO: delete garbage global scaling variables bullshit
WIDTH = 800
HEIGHT = 800
WIDTH_SCALED = 36 / 400 * WIDTH
HEIGHT_SCALED = 27 / 450 * HEIGHT
HEALTHBAR_FULL_WIDTH_SCALED = 64 / 192 * WIDTH * 0.7
HEALTHBAR_FULL_HEIGHT_SCALED = 9 / 192 * HEIGHT * 0.7
HEALTHBAR_BAD_WIDTH_SCALED = 6 / 192 * WIDTH * 0.7
HEALTHBAR_BAD_HEIGHT_SCALED = HEALTHBAR_FULL_HEIGHT_SCALED
HEALTHBAR_FUCKING_BLACK_PIXEL_WIDTH_OR_SOMETHING_SCALED = 3
HEALTHBAR_HEARTH_WIDTH_SCALED = 30
HEALTHBAR_HEARTH_HEIGHT_SCALED = 27
PROJECTILE_WIDTH_SCALED = 8 / 400 * WIDTH
PROJECTILE_HEIGHT_SCALED = 15 / 450 * HEIGHT
PROJECTILE_VELOCITY = 15
PLAYER_PROJECTILE_DELAY = 500
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = 0.12

surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
pygame.display.set_icon(pygame.image.load(r"./images/icon.png"))

class Images:
	background = pygame.transform.scale(pygame.image.load(r"./images/background.png"), (WIDTH, HEIGHT))
	healthbar_full = pygame.transform.scale(pygame.image.load(r"./images/healthbar_full.png"), (HEALTHBAR_FULL_WIDTH_SCALED, HEALTHBAR_FULL_HEIGHT_SCALED))
	healthbar_bad = pygame.transform.scale(pygame.image.load(r"./images/healthbar_bad.png"), (HEALTHBAR_BAD_WIDTH_SCALED, HEALTHBAR_BAD_HEIGHT_SCALED))
	healthbar_hearth = pygame.transform.scale(pygame.image.load(r"./images/healthbar_hearth.png"), (HEALTHBAR_HEARTH_WIDTH_SCALED, HEALTHBAR_HEARTH_HEIGHT_SCALED))
	healthbar_hearth_flipped = pygame.transform.flip(healthbar_hearth, True, True)
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

	def draw(self):
		surface.blit(Images.background, (0, 0))

	def get_player_by_id(self, id):
		for e in self.get_all_entities_of_type(Entity.Type.PLAYER):
			if e.id == id:
				return e

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

	def update(self):
		pass

class Player(Entity):
	def __init__(self, id):
		self.id = id
		self.last_projectile = 0
		self.max_health = 13
		self.health = 13
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

	def request_projectile(self):
		if self.last_projectile + PLAYER_PROJECTILE_DELAY < pygame.time.get_ticks():
			self.last_projectile = pygame.time.get_ticks()
			position = self.position.copy()
			position.x += self.image.get_width() // 2
			velocity = pygame.math.Vector2(0, -PROJECTILE_VELOCITY if self.id == 1 else PROJECTILE_VELOCITY)
			projectile = Projectile(self.id, position, velocity)
			return projectile
		else:
			return None

	def draw(self):
		super().draw()
		if self.id == 1:
			wm = Images.healthbar_hearth.get_width() + 5 + Images.healthbar_full.get_width()
			hp = max(Images.healthbar_full.get_height(), Images.healthbar_hearth.get_height())
			hm = min(Images.healthbar_full.get_height(), Images.healthbar_hearth.get_height())
			xl = (WIDTH - wm) // 2
			xr = xl + Images.healthbar_hearth.get_width() + 5
			yp = HEIGHT - hp - 5
			ym = yp + (hp - hm) // 2
			surface.blit(Images.healthbar_hearth, (xl, ym))
			surface.blit(Images.healthbar_full, (xr, yp))
			for i in range(self.health, self.max_health):
				surface.blit(Images.healthbar_bad, (xr + (Images.healthbar_bad.get_width() * i - HEALTHBAR_FUCKING_BLACK_PIXEL_WIDTH_OR_SOMETHING_SCALED * i), yp))
		elif self.id == 2:
			wm = Images.healthbar_full.get_width() + 5 + Images.healthbar_hearth_flipped.get_width()
			hp = max(Images.healthbar_full.get_height(), Images.healthbar_hearth_flipped.get_height())
			hm = min(Images.healthbar_full.get_height(), Images.healthbar_hearth_flipped.get_height())
			xl = (WIDTH - wm) // 2
			xr = xl + Images.healthbar_full.get_width() + 5
			yp = 5
			ym = yp + (hp - hm) // 2
			surface.blit(Images.healthbar_full, (xl, ym))
			surface.blit(Images.healthbar_hearth_flipped, (xr, yp))
			for i in range(self.max_health - self.health):
				surface.blit(Images.healthbar_bad, (xl + (Images.healthbar_bad.get_width() * i - HEALTHBAR_FUCKING_BLACK_PIXEL_WIDTH_OR_SOMETHING_SCALED * i), yp))

class Projectile(Entity):
	def __init__(self, owner_id, position, velocity):
		self.owner_id = owner_id
		self.image = getattr(Images, f"projectile_{self.owner_id}")
		position.x -= self.image.get_width() // 2
		super().__init__(Entity.Type.PROJECTILE, self.image, position, velocity)

	def update(self):
		self.position += self.velocity

	def is_out_of_bounds(self, bounds):
		x1, y1, x2, y2 = bounds
		if not (x1 < self.position.x < x2 and y1 < self.position.y < y2):
			game.delete_entity(self)

	def does_collide_with_player(self, player):
		# TODO: fix when deltatime is low: use raytracing
		r1x1 = self.position.x
		r1x2 = self.position.x + self.image.get_width()
		r1y1 = self.position.y
		r1y2 = self.position.y + self.image.get_height()
		r2x1 = player.position.x + player.image.get_width()
		r2x2 = player.position.x
		r2y1 = player.position.y + player.image.get_height()
		r2y2 = player.position.y
		return not (r1x2 < r2x2 or r1y2 < r2y2 or r1x1 > r2x1 or r1y1 > r2y2)

class Debug: # debugging shit
	enabled = True
	font = pygame.font.SysFont("arial.ttf", 24)
	_row_offset_y = 0
	_color = (255, 0, 0)

	def new_frame():
		Debug._row_offset_y = 0

	def draw_info(surface, text):
		fw, fh = Debug.font.size(text)
		surface.blit(Debug.font.render(text, True, Debug._color), (0, Debug._row_offset_y))
		Debug._row_offset_y += fh

	def draw_box(surface, box):
		pygame.draw.rect(surface, Debug._color, box, 1)

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
		if (p := game.player1.request_projectile()) is not None:
			game.append_entity(p)
	if (pressed_keys[pygame.K_RIGHT]):
		game.player2.move_left()
	if (pressed_keys[pygame.K_LEFT]):
		game.player2.move_right()
	if (pressed_keys[pygame.K_UP]):
		if (p := game.player2.request_projectile()) is not None:
			game.append_entity(p)

	game.draw()
	for entity in game.get_all_entities():
		entity.update()
		entity.draw()
		if entity.type == Entity.Type.PROJECTILE:
			if entity.is_out_of_bounds([0, 0, WIDTH, HEIGHT]):
				game.delete_entity(entity)
			hitter = game.get_player_by_id(entity.owner_id)
			target = game.get_player_by_id(3 - entity.owner_id)
			if entity.does_collide_with_player(target):
				print(f"Player {hitter.id} hit Player {target.id}")
				target.health -= 1
				game.delete_entity(entity)

	if Debug.enabled: # debugging shit
		Debug.new_frame()
		Debug.draw_info(surface, f"FPS: {round(clock.get_fps())}")
		Debug.draw_info(surface, f"FT (DT): {round(clock.get_time())}ms")
		Debug.draw_info(surface, f"FCT: {round(clock.get_rawtime())}ms")
		Debug.draw_info(surface, f"EC: {len(game._entities)}")
		Debug.draw_info(surface, f"MP: {pygame.mouse.get_pos()}")
		for entity in game.get_all_entities():
			Debug.draw_box(surface, (*entity.position, entity.image.get_width(), entity.image.get_height()))
	
	pygame.display.update()
	surface.fill((0, 0, 0))
	deltatime = clock.tick(60)

pygame.display.quit()
pygame.quit()

sys.exit(0)