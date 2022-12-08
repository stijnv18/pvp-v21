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
BXSCALE= BX * WIDTH		  #width bullet scaled
BYSCALE = BY * HEIGHT	  #height bullet scaled
WSCALED = PSCALEW*WIDTH   #width player scaled
HSCALED = PSCALEH*HEIGHT  #heigt palyer scaled
P2SCALE = 50 / 450
P1SCALE = 430 / 450
P1SCALED = P1SCALE * HEIGHT
P2SCALED = P2SCALE * HEIGHT
HPSCALEDW = 64 / 192 * WIDTH * 0.7
HPSCALEDH = 9 / 192 * HEIGHT * 0.7
REDSCALEW = 4 / 192 * WIDTH * 0.7
REDSCALEH = 7 / 192 * HEIGHT * 0.7

FramePerSec = pygame.time.Clock()

visible = (0,0,0,100)
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load('crabbackground.png').convert()
HPplayer1 = pygame.image.load('groenbar.png')
HPplayer1 = pygame.transform.flip(HPplayer1,True,True)
HPplayer2 = pygame.image.load('groenbar.png')
HPn = pygame.image.load('roodblokje.png')
HPn2 = pygame.image.load('roodblokje.png')
HPn2 = pygame.transform.flip(HPn2,True,True)
pygame.display.set_caption("Game")
icon = pygame.image.load('p1crab.png').convert()
icon = pygame.transform.scale(icon,(23,32))
pygame.display.set_icon(icon)
cd3=pygame.image.load('3.png')
cd2=pygame.image.load('2.png')
cd1=pygame.image.load('1.png')

 
class Player1(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__() 
		self.player = pygame.image.load('p1crab.png').convert_alpha()
		self.player = pygame.transform.scale(self.player,(WSCALED,HSCALED))
		self.surf = pygame.Surface((WSCALED, HSCALED),SRCALPHA)
		self.surf.blit(self.player,(0,0))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((WIDTH/2, P1SCALED))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.active = False
 
	def moveplayer1(self,pewpewpew):
		self.acc = vec(0,0)
		global timelastfireforplayer2
		pressed_keys = pygame.key.get_pressed()     
		if self.active == True:       
			if pressed_keys[K_q] or pressed_keys[K_a]:
				self.acc.x = -ACC
			if pressed_keys[K_d]:
				self.acc.x = ACC
			if pressed_keys[K_z] or pressed_keys[K_w]:
				if time.time()-timelastfireforplayer2>0.05:
					timelastfireforplayer2 = time.time()
					updateposbulletlist=list(self.pos)
					updateposbulletlist[0]=updateposbulletlist[0]-(BXSCALE/2)
					updateposbulletlist=tuple(updateposbulletlist)
					pewpewpew.append(shootsprite(updateposbulletlist,False))

		self.acc.x += self.vel.x * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
			
		if self.pos.x > WIDTH-WSCALED-10:
			self.pos.x = WIDTH-WSCALED-10
		if self.pos.x < 0+WSCALED+10: 
			self.pos.x = 0+WSCALED+10
			
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
		self.active = False
 
	def moveplayer2(self,pewpewpew):
		
			self.acc = vec(0,0)
			global timelastfire
			pressed_keys = pygame.key.get_pressed()  
			if self.active == True:        
				if pressed_keys[K_LEFT]:
					self.acc.x = -ACC
				if pressed_keys[K_RIGHT]:
					self.acc.x = ACC
				if pressed_keys[K_SPACE]:
					
					if time.time()-timelastfire>0.05:
						timelastfire = time.time()
						updateposbulletlist=list(self.pos)
						updateposbulletlist[0]=updateposbulletlist[0]-(BXSCALE/2)
						updateposbulletlist=tuple(updateposbulletlist)
						pewpewpew.append(shootsprite(updateposbulletlist,True))

			self.acc.x += self.vel.x * FRIC
			self.vel += self.acc
			self.pos += self.vel + 0.5 * self.acc
				
			if self.pos.x > WIDTH-WSCALED-10:
				self.pos.x = WIDTH-WSCALED-10
			if self.pos.x < 0+WSCALED+10:
				self.pos.x = 0+WSCALED+10
				
			self.rect.midbottom = self.pos    




class shootsprite(pygame.sprite.Sprite):
	def __init__(self,poss,facing):
		super().__init__()
		self.poss = poss
		self.facing = facing
		self.vel = 10

		if facing == True:


			mypos = list(poss)
			mypos[1]+=10
			mypos[1]=round(mypos[1],0)
			poss = tuple(mypos)
			self.poss = poss
			self.bullet = pygame.image.load('projectiel2.png').convert_alpha()
			self.bullet = pygame.transform.scale(self.bullet,(BXSCALE,BYSCALE))

			self.surf = pygame.Surface((WIDTH,HEIGHT),SRCALPHA)#36,27
			self.surf.blit(self.bullet,poss)
			self.rect = self.surf.get_rect() 
		elif facing == False:
			mypos = list(poss)
			mypos[1]=mypos[1]-self.vel
			mypos[1]=round(mypos[1],0)
			poss = tuple(mypos)
			self.poss = poss
			if poss[1] < 0:
				self.kill()
			else:	
				self.bullet = pygame.image.load('projectiel1.png').convert_alpha()
				self.bullet = pygame.transform.scale(self.bullet,(BXSCALE,BYSCALE))

				self.surf = pygame.Surface((WIDTH,HEIGHT),SRCALPHA )#36,27
				self.surf.blit(self.bullet,poss)
				self.rect = self.surf.get_rect() 

def checkplayerhit(player,list):
	for bullet in list:

		bulletposx = round(bullet.poss[0],0)
		bulletposy = round(bullet.poss[1],0)

		playerposx = round(player.pos[0],0)
		playerposy = round(player.pos[1],0)

		Color = (255,255,255)
		rect = pygame.Rect((playerposx -(WSCALED/2)),(playerposy -(HSCALED)),WSCALED,HSCALED)
		pygame.draw.rect(displaysurface,Color,rect,2)

		left = (playerposx -(WSCALED/2))
		top = (playerposy -(HSCALED))
		right = left + WSCALED
		bottem = top + HSCALED

		bulletLeft = (bulletposx)
		bulletRight = bulletLeft+BXSCALE
		bulletTop = (bulletposy)
		bulletBottem = bulletTop + BYSCALE

		if(left<=bulletLeft<=right or left<=bulletRight<=right):
			if(top<=bulletBottem<=bottem or top <bulletTop <=bottem):
				return True
	return False


def hit1(player):
	while player == 1:
		for i in range(0,hp1):
			displaysurface.blit(pygame.transform.smoothscale(HPn,(REDSCALEW+1,REDSCALEH)), (480-i*REDSCALEW,HEIGHT-26))
		hp1 += 1
		while hp1 == 13:
			return 2
		break
	while player == 2:
		for i in range(0,hp2):
			displaysurface.blit(pygame.transform.smoothscale(HPn2,(REDSCALEW+1,REDSCALEH)),(320+i*REDSCALEW,30))
		hp2 += 1
		while hp2 == 13:
			
			return 1
		break
		 
def start(): # 3,2,1 afbeeldingen laten zien en dan movement/schieten unlocken
	global timecdstart 
	if time.time() - timecdstart < 1:
		displaysurface.blit(cd3,(350,350))
	if time.time() - timecdstart > 1 and time.time() - timecdstart < 2:
		displaysurface.blit(cd2,(350,350))
	if time.time() - timecdstart > 2 and time.time() - timecdstart < 3:
		displaysurface.blit(cd1,(350,350))
		P1.active = True
		P2.active = True
	





def restart(P1,P2): #crabben terug naar originele positie + movement/schieten locken + HP refill + start countdown sequence 
	P1.pos = vec((WIDTH/2, P1SCALED))
	P2.pos = vec((WIDTH/2, P2SCALED))
	P1.active = False
	P2.active = False
	start()




P1 = Player1()
P2 = Player2()

sh = shootsprite((1000,10),True)
all_sprites = pygame.sprite.Group()
all_sprites.add(P2)
all_sprites.add(P1)
#all_sprites.add(sh)

pewpewpew=[]
timelastfire = 0 
timelastfireforplayer2 = 0
timecdstart = time.time()
remove =[]
hp1 = 0
hp2 = 0

while True:
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
   

	for i in range(0,len(pewpewpew)):
		if pewpewpew[i].poss[1] <800 and pewpewpew[i].poss[1]>0:
			pewpewpew[i].__init__((pewpewpew[i].poss[0],pewpewpew[i].poss[1]),pewpewpew[i].facing)
				 
		else:
			remove.append(pewpewpew[i])
	for rem in remove:
		try:
			pewpewpew.remove(rem)
			all_sprites.remove(rem)
		except:
			pass

	for sprite in pewpewpew:
		all_sprites.add(sprite)
	displaysurface.fill((255,255,255))
	displaysurface.blit(pygame.transform.smoothscale(bg,(displaysurface.get_size())),(0,0))	
	displaysurface.blit(pygame.transform.smoothscale(HPplayer1,(HPSCALEDW,HPSCALEDH)), (displaysurface.get_rect().centerx-HPSCALEDW/2,30))
	displaysurface.blit(pygame.transform.smoothscale(HPplayer2,(HPSCALEDW,HPSCALEDH)), (displaysurface.get_rect().centerx-HPSCALEDW/2,HEIGHT-30))
	
	
	P1.moveplayer1(pewpewpew)
	P2.moveplayer2(pewpewpew)
	playerposx = round(P1.pos[0],0)
	playerposy = round(P1.pos[1],0)


	Color = (255,0,0)
	rect = pygame.Rect((playerposx -(WSCALED/2)),(playerposy -(HSCALED)),WSCALED,HSCALED)
	pygame.draw.rect(displaysurface,Color,rect,2)

	for pew in pewpewpew:
		bulletposx = round(pew.poss[0],0)
		bulletposy = round(pew.poss[1],0)
		bulletLeft = (bulletposx)
		bulletRight = bulletLeft+BXSCALE
		bulletTop = (bulletposy)
		bulletBottem = bulletTop + BYSCALE
		Color = (255,0,0)
		rect = pygame.Rect((bulletposx),(bulletposy),BXSCALE,BYSCALE)
		pygame.draw.rect(displaysurface,Color,rect,2)

	#P1.hitplayer(P1,pewpewpew)
	## hit player check
	checkplayerhit(P2,pewpewpew)


	all_sprites.add(P2)
	all_sprites.add(P1) 
	for entity in all_sprites:

		try:
			displaysurface.blit(entity.surf, entity.rect)
		except AttributeError:
			print("error")
	start()
	pygame.display.update()
	FramePerSec.tick(FPS)