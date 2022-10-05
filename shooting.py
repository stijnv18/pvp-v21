import pygame
from pygame.locals import *
import sys
 
pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
PHEIGHT = 27
PWIDTH = 36
PSCALEH = 27 / 450
PSCALEW = 36 / 400
WSCALED = PSCALEW*WIDTH
HSCALED = PSCALEH*HEIGHT
P2SCALE = 40 / 450
P1SCALE = 440 / 450
P1SCALED = P1SCALE * HEIGHT
P2SCALED = P2SCALE * HEIGHT
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load('background.jpg')
pygame.display.set_caption("Game")
icon = pygame.image.load('p1crab.png')
icon = pygame.transform.scale(icon,(23,32))
pygame.display.set_icon(icon)
 
class Player1(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__() 
		player = pygame.image.load('p1crab.png')
		player = pygame.transform.scale(player,(WSCALED,HSCALED))
		self.surf = pygame.Surface((WSCALED, HSCALED),SRCALPHA)
		self.surf.blit(player,(0,0))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((WIDTH/2, P1SCALED))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
 
	def moveplayer1(self):
		self.acc = vec(0,0)

		pressed_keys = pygame.key.get_pressed()            
		if pressed_keys[K_q]:
			self.acc.x = -ACC
		if pressed_keys[K_d]:
			self.acc.x = ACC
				
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
			
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH
			
		self.rect.midbottom = self.pos    
 



class Player2(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__() 
		player = pygame.image.load('p2crab.png')
		player = pygame.transform.scale(player,(WSCALED,HSCALED))
		self.surf = pygame.Surface((WSCALED, HSCALED),SRCALPHA)
		self.surf.blit(player,(0,0))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((WIDTH/2, P2SCALED))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
 
	def moveplayer2(self,pewpew):
		self.acc = vec(0,0)

		pressed_keys = pygame.key.get_pressed()            
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC
		if pressed_keys[K_SPACE]:
			if len(pewpew) < 10:
				pewpew.append(shoot(self.pos,True))
				
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
			
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH
			
		self.rect.midbottom = self.pos    


class shoot(object): ##### sprite rendering
	def __init__(self,poss,facing):
		super().__init__() 
		self.poss =poss
		self.facing = facing
		self.vel = 10

class shootsprite(pygame.sprite.Sprite):
	def __init__(self,poss):
		super().__init__()
		mypos = list(poss.poss)
		print(mypos)
		mypos[1]+=10
		poss.poss = tuple(mypos)

		bullet = pygame.image.load('p1crab.png')
		bullet = pygame.transform.scale(bullet,(WSCALED,HSCALED))
		self.surf = pygame.Surface((poss.poss[0], poss.poss[1]),SRCALPHA)#36,27
		self.surf.blit(bullet,(0,0))
		self.rect = self.surf.get_rect()
		# self.rect =  pygame.draw.circle(surface=self.surf,color=(255,255,0),center=poss.poss,radius=5)
		

P1 = Player1()
P2 = Player2()
initpew = shoot((0,100000),True)
sh = shootsprite(initpew)
all_sprites = pygame.sprite.Group()
all_sprites.add(P2)
all_sprites.add(P1)
all_sprites.add(sh)
pewpew = []
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	for pew in pewpew:
		
		if pew.poss[1] <500 and pew.poss[1]>0:
			#pew.poss[1]+=pew.vel
			sh.__init__(pew)
		else:
			pewpew.pop(pewpew.index(pew))

	displaysurface.fill((255,255,255))
	displaysurface.blit(pygame.transform.smoothscale(bg,(displaysurface.get_size())),(0,0))	

	
	P1.moveplayer1()
	P2.moveplayer2(pewpew)
	for entity in all_sprites:
		try:
			displaysurface.blit(entity.surf, entity.rect)
		except AttributeError:
			print("error")
	
	pygame.display.update()
	FramePerSec.tick(FPS)