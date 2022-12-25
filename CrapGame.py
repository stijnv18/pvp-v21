import sys # built-in python module
import pygame # pip install pygame
import shapely.geometry.polygon # pip install shapely

# TODO: use deltatime for movement
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
FPS = 60

surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CrapGame")
pygame.display.set_icon(pygame.image.load(r"./textures/icon.png"))

class Controls:
	P1_LEFT = 4
	P1_RIGHT = 7
	P1_SHOOT = 26
	P2_LEFT = 80
	P2_RIGHT = 79
	P2_SHOOT = 82

class Textures:
	mainmenu = pygame.transform.scale(pygame.image.load(r"./textures/mainmenu.png"), (WIDTH, HEIGHT))
	background = pygame.transform.scale(pygame.image.load(r"./textures/background.png"), (WIDTH, HEIGHT))
	healthbar_full = pygame.transform.scale(pygame.image.load(r"./textures/healthbar_full.png"), (HEALTHBAR_FULL_WIDTH_SCALED, HEALTHBAR_FULL_HEIGHT_SCALED))
	healthbar_bad = pygame.transform.scale(pygame.image.load(r"./textures/healthbar_bad.png"), (HEALTHBAR_BAD_WIDTH_SCALED, HEALTHBAR_BAD_HEIGHT_SCALED))
	healthbar_hearth = pygame.transform.scale(pygame.image.load(r"./textures/healthbar_hearth.png"), (HEALTHBAR_HEARTH_WIDTH_SCALED, HEALTHBAR_HEARTH_HEIGHT_SCALED))
	healthbar_hearth_flipped = pygame.transform.flip(healthbar_hearth, True, True)
	countdown_3 = pygame.transform.scale(pygame.image.load(r"./textures/countdown_3.png"), (198, 120))
	countdown_2 = pygame.transform.scale(pygame.image.load(r"./textures/countdown_2.png"), (198, 120))
	countdown_1 = pygame.transform.scale(pygame.image.load(r"./textures/countdown_1.png"), (198, 120))
	restart = pygame.transform.scale(pygame.image.load(r"./textures/restart.png"), (280, 34))
	player_1 = pygame.transform.scale(pygame.image.load(r"./textures/player_1.png"), (WIDTH_SCALED, HEIGHT_SCALED))
	player_2 = pygame.transform.scale(pygame.image.load(r"./textures/player_2.png"), (WIDTH_SCALED, HEIGHT_SCALED))
	projectile_1 = pygame.transform.scale(pygame.image.load(r"./textures/projectile_1.png"), (PROJECTILE_WIDTH_SCALED, PROJECTILE_HEIGHT_SCALED))
	projectile_2 = pygame.transform.scale(pygame.image.load(r"./textures/projectile_2.png"), (PROJECTILE_WIDTH_SCALED, PROJECTILE_HEIGHT_SCALED))

class Game:
	class State:
		MAINMENU = 0
		COUNTDOWN = 1
		PLAYING = 2
		RESTART = 3

	def __init__(self):
		self.state = Game.State.MAINMENU
		self.player1 = Player(1)
		self.player2 = Player(2)
		self._entities = [self.player1, self.player2]
		self._countdown = 0

	def start_countdown(self):
		self.state = Game.State.COUNTDOWN
		self._countdown = pygame.time.get_ticks() - 1000

	def draw(self):
		if (self.state == Game.State.MAINMENU):
			surface.blit(Textures.mainmenu, (0, 0))
		else:
			surface.blit(Textures.background, (0, 0))

	def draw_darker_overlay(self):
		s = pygame.Surface((WIDTH, HEIGHT))
		s.fill((0, 0, 0))
		s.set_alpha(127)
		surface.blit(s, (0, 0))

	def process_gamestate(self):
		if self.state == Game.State.RESTART:
			self.draw_darker_overlay()
			surface.blit(Textures.restart, ((WIDTH - Textures.restart.get_width()) // 2, (HEIGHT - Textures.restart.get_height()) // 2))
		elif self.state == Game.State.COUNTDOWN:
			self.draw_darker_overlay()
			if self._countdown + 4000 < pygame.time.get_ticks():
				self.state = Game.State.PLAYING
			elif self._countdown + 3000 < pygame.time.get_ticks():
				surface.blit(Textures.countdown_1, ((WIDTH - Textures.countdown_1.get_width()) // 2, (HEIGHT - Textures.countdown_1.get_height()) // 2))
			elif self._countdown + 2000 < pygame.time.get_ticks():
				surface.blit(Textures.countdown_2, ((WIDTH - Textures.countdown_2.get_width()) // 2, (HEIGHT - Textures.countdown_2.get_height()) // 2))
			elif self._countdown + 1000 < pygame.time.get_ticks():
				surface.blit(Textures.countdown_3, ((WIDTH - Textures.countdown_3.get_width()) // 2, (HEIGHT - Textures.countdown_3.get_height()) // 2))

	def get_player_by_id(self, id):
		for e in self.get_all_entities_of_type(Entity.Type.PLAYER):
			if e.id == id:
				return e

	def get_all_entities_of_type(self, type):
		return [e for e in self.get_all_entities() if e.type == type]

	def get_all_entities(self):
		return self._entities

	def create_entity(self, entity):
		self._entities.append(entity)

	def delete_entity(self, entity):
		self._entities.remove(entity)

class Entity:
	class Type:
		PLAYER = 0
		PROJECTILE = 1

	def __init__(self, type, texture, position, hitbox, velocity=None, acceleration=None):
		self.type = type
		self.texture = texture
		self.position = position
		self.hitbox = hitbox
		self.velocity = velocity if velocity is not None else pygame.math.Vector2(0, 0)
		self.acceleration = acceleration if acceleration is not None else pygame.math.Vector2(0, 0)
		self.visible = True

	def draw(self):
		if self.visible:
			surface.blit(self.texture, self.position)

	def does_collide_with(self, entity):
		p1 = shapely.geometry.polygon.Polygon(tuple(map(lambda p: tuple(map(lambda a, b: a + b, p, self.position)), self.hitbox)))
		p2 = shapely.geometry.polygon.Polygon(tuple(map(lambda p: tuple(map(lambda a, b: a + b, p, entity.position)), entity.hitbox)))
		return p1.overlaps(p2)

	def update(self):
		pass

class Player(Entity):
	def __init__(self, id):
		self.id = id
		self.last_projectile = 0
		self.max_health = 13
		self.health = 13
		texture = getattr(Textures, f"player_{self.id}")
		position = pygame.math.Vector2(((WIDTH - texture.get_width()) // 2, (35 if id == 2 else HEIGHT - texture.get_height() - 35)))
		super().__init__(Entity.Type.PLAYER, texture, position, ((0, 0), (texture.get_width(), 0), (texture.get_width(), texture.get_height()), (0, texture.get_height())))

	def update(self):
		self.acceleration.x += self.velocity.x * -PLAYER_FRICTION
		self.velocity += self.acceleration
		self.position += self.velocity + PLAYER_ACCELERATION * self.acceleration
		
		if self.position.x > WIDTH - self.texture.get_width() - WIDTH_SCALED // 2 - 5:
			self.position.x = WIDTH - self.texture.get_width() - WIDTH_SCALED // 2 - 5
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
			position.x += self.texture.get_width() // 2
			velocity = pygame.math.Vector2(0, -PROJECTILE_VELOCITY if self.id == 1 else PROJECTILE_VELOCITY)
			projectile = Projectile(self.id, position, velocity)
			return projectile
		else:
			return None

	def take_damage(self, amount):
		self.health -= amount
		if self.health <= 0:
			self.health = 0
			return True
		return False

	def draw(self):
		super().draw()
		if self.id == 1:
			wm = Textures.healthbar_hearth.get_width() + 5 + Textures.healthbar_full.get_width()
			hp = max(Textures.healthbar_full.get_height(), Textures.healthbar_hearth.get_height())
			hm = min(Textures.healthbar_full.get_height(), Textures.healthbar_hearth.get_height())
			xl = (WIDTH - wm) // 2
			xr = xl + Textures.healthbar_hearth.get_width() + 5
			yp = HEIGHT - hp - 5
			ym = yp + (hp - hm) // 2
			surface.blit(Textures.healthbar_hearth, (xl, ym))
			surface.blit(Textures.healthbar_full, (xr, yp))
			for i in range(self.health, self.max_health):
				surface.blit(Textures.healthbar_bad, (xr + (Textures.healthbar_bad.get_width() * i - HEALTHBAR_FUCKING_BLACK_PIXEL_WIDTH_OR_SOMETHING_SCALED * i), yp))
		elif self.id == 2:
			wm = Textures.healthbar_full.get_width() + 5 + Textures.healthbar_hearth_flipped.get_width()
			hp = max(Textures.healthbar_full.get_height(), Textures.healthbar_hearth_flipped.get_height())
			hm = min(Textures.healthbar_full.get_height(), Textures.healthbar_hearth_flipped.get_height())
			xl = (WIDTH - wm) // 2
			xr = xl + Textures.healthbar_full.get_width() + 5
			yp = 5
			ym = yp + (hp - hm) // 2
			surface.blit(Textures.healthbar_full, (xl, ym))
			surface.blit(Textures.healthbar_hearth_flipped, (xr, yp))
			for i in range(self.max_health - self.health):
				surface.blit(Textures.healthbar_bad, (xl + (Textures.healthbar_bad.get_width() * i - HEALTHBAR_FUCKING_BLACK_PIXEL_WIDTH_OR_SOMETHING_SCALED * i), yp))

class Projectile(Entity):
	def __init__(self, owner_id, position, velocity):
		self.owner_id = owner_id
		self.texture = getattr(Textures, f"projectile_{self.owner_id}")
		position.x -= self.texture.get_width() // 2
		super().__init__(Entity.Type.PROJECTILE, self.texture, position, ((0, 0), (self.texture.get_width(), 0), (self.texture.get_width(), self.texture.get_height()), (0, self.texture.get_height())), velocity)

	def update(self):
		self.position += self.velocity

	def is_out_of_bounds(self, bounds):
		x1, y1, x2, y2 = bounds
		if not (x1 < self.position.x < x2 and y1 < self.position.y < y2):
			game.delete_entity(self)

class Debug: # debugging shit
	enabled = False
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
pressed_keys = [] # TODO: gebruik unicode ipv scancode?

running = True
while running:
	for event in pygame.event.get():
		match event.type:
			case pygame.QUIT:
				running = False
			case pygame.KEYDOWN:
				pressed_keys.append(event.scancode)
				if event.key == pygame.K_r:
					if game.state == Game.State.RESTART:
						game = Game()
						game.start_countdown()
				if event.key == pygame.K_SPACE:
					if game.state == Game.State.MAINMENU:
						game.start_countdown()
				if event.key == pygame.K_F3:
					Debug.enabled = not Debug.enabled
			case pygame.KEYUP:
				pressed_keys.remove(event.scancode)

	# TODO: convert naar match-case
	if game.state == Game.State.PLAYING:
		if Controls.P1_LEFT in pressed_keys:
			game.player1.move_left()
		if Controls.P1_RIGHT in pressed_keys:
			game.player1.move_right()
		if Controls.P1_SHOOT in pressed_keys:
			if (p := game.player1.request_projectile()) is not None:
				game.create_entity(p)
		if Controls.P2_LEFT in pressed_keys:
			game.player2.move_left()
		if Controls.P2_RIGHT in pressed_keys:
			game.player2.move_right()
		if Controls.P2_SHOOT in pressed_keys:
			if (p := game.player2.request_projectile()) is not None:
				game.create_entity(p)

	game.draw()
	for entity in game.get_all_entities():
		if game.state == Game.State.PLAYING:
			entity.update()
		if game.state != Game.State.MAINMENU:
			entity.draw()
		if entity.type == Entity.Type.PROJECTILE:
			if entity.is_out_of_bounds([0, 0, WIDTH, HEIGHT]):
				game.delete_entity(entity)
			target = game.get_player_by_id(3 - entity.owner_id)
			if entity.does_collide_with(target):
				if target.take_damage(1):
					game.state = Game.State.RESTART
				game.delete_entity(entity)
	game.process_gamestate()

	if Debug.enabled: # debugging shit
		Debug.new_frame()
		Debug.draw_info(surface, f"FPS: {round(clock.get_fps())}")
		Debug.draw_info(surface, f"FT (DT): {round(clock.get_time())}ms")
		Debug.draw_info(surface, f"FCT: {round(clock.get_rawtime())}ms")
		Debug.draw_info(surface, f"EC: {len(game._entities)}")
		Debug.draw_info(surface, f"MP: {pygame.mouse.get_pos()}")
		for entity in game.get_all_entities():
			Debug.draw_box(surface, (*entity.position, entity.texture.get_width(), entity.texture.get_height()))

	pygame.display.update()
	surface.fill((0, 0, 0))
	deltatime = clock.tick(FPS)

pygame.display.quit()
pygame.quit()

sys.exit(0)