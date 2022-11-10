from queue import Empty
import pygame
from pygame.locals import *
import sys
import time
pygame.init()
 
vec = pygame.math.Vector2 
HEIGHT = 800
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 60
BX=8/400
BY=15/450
PHEIGHT = 27
PWIDTH = 36
PSCALEH = 27 / 450
PSCALEW = 36 / 400
BXSCALE= BX * WIDTH
BYSCALE = BY * HEIGHT
WSCALED = PSCALEW*WIDTH
HSCALED = PSCALEH*HEIGHT
P2SCALE = 40 / 450
P1SCALE = 440 / 450
P1SCALED = P1SCALE * HEIGHT
P2SCALED = P2SCALE * HEIGHT
FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load('background.jpg').convert()
pygame.display.set_caption("Game")
icon = pygame.image.load('p1crab.png').convert()
icon = pygame.transform.scale(icon,(23,32))
pygame.display.set_icon(icon)
 
class Player1(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__() 
		player = pygame.image.load('p1crab.png').convert_alpha()
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
		player = pygame.image.load('p2crab.png').convert_alpha()
		player = pygame.transform.scale(player,(WSCALED,HSCALED))
		self.surf = pygame.Surface((WSCALED, HSCALED),SRCALPHA)
		self.surf.blit(player,(0,0))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((WIDTH/2, P2SCALED))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
 
	def moveplayer2(self,pewpewpew):
		self.acc = vec(0,0)
		global timelastfire
		pressed_keys = pygame.key.get_pressed()            
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = ACC
		if pressed_keys[K_SPACE]:
			if len(pewpewpew) < 10:
			
				if time.time()-timelastfire>0.5:
					timelastfire = time.time()
					
					pewpewpew.append(shootsprite(self.pos,True))
			else:

				if time.time()-timelastfire>0.5:
					timelastfire = time.time()
					for pew in pewpewpew: 
						if pew.poss[1] >HEIGHT and pew.poss[1]>0:
							
							pew.poss=self.pos
							break
			
		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
			
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH
			
		self.rect.midbottom = self.pos    




class shootsprite(pygame.sprite.Sprite):
	def __init__(self,poss,facing):
		super().__init__()
		self.poss = poss
		self.facing = facing
		self.vel = 10




		mypos = list(poss)
		mypos[1]+=self.vel
		mypos[1]=round(mypos[1],0)
		poss = tuple(mypos)

		bullet = pygame.image.load('projectiel2.png').convert_alpha()
		bullet = pygame.transform.scale(bullet,(BXSCALE,BYSCALE))

		self.surf = pygame.Surface((WIDTH,HEIGHT),SRCALPHA)#36,27
		self.surf.blit(bullet,poss)
		self.rect = self.surf.get_rect() 
		# self.rect =  pygame.draw.circle(surface=self.surf,color=(255,255,0),center=poss.poss,radius=5)




P1 = Player1()
P2 = Player2()

sh = shootsprite((1000,10),True)
all_sprites = pygame.sprite.Group()
all_sprites.add(P2)
all_sprites.add(P1)
#all_sprites.add(sh)

pewpewpew=[]
timelastfire = 0 
remove =[]
while True:


	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
   
	for i in range(0,len(pewpewpew)):
		pass

	for i in range(0,len(pewpewpew)):

		print(pewpewpew[i].facing)
		if pewpewpew[i].poss[1] <HEIGHT and pewpewpew[i].poss[1]>0:
			pewpewpew[i].__init__((pewpewpew[i].poss[0],pewpewpew[i].poss[1]+10),pewpewpew[i].facing)
			pass       
		else:
			remove.append(i)
	
	for sprite in pewpewpew:
		all_sprites.add(sprite)
	displaysurface.fill((255,255,255))
	displaysurface.blit(pygame.transform.smoothscale(bg,(displaysurface.get_size())),(0,0))	

	
	P1.moveplayer1()
	P2.moveplayer2(pewpewpew)
	#print(all_sprites.sprites())
	for entity in all_sprites:

		try:
			displaysurface.blit(entity.surf, entity.rect)
		except AttributeError:
			print("error")
	
	pygame.display.update()
	FramePerSec.tick(FPS)