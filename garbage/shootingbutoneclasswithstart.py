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

def scaler(W,H,OW,OH):
    scaledW = W / OW * WIDTH
    scaledH = H / OH * HEIGHT
    return scaledW, scaledH

#player scaling
WSCALED,HSCALED = scaler(36,27,400,450)

#HP
HPSCALEDW,HPSCALEDH = scaler(64,9,192,192)

#red HP
REDSCALEW,REDSCALEH = scaler(4,7,192,192)

#countdown
CDSCALEW,CDSCALEH = scaler(66,40,192,192)

#bullet
BXSCALE, BYSCALE=scaler(8,15,400,450)


FramePerSec = pygame.time.Clock()

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
		self.player = pygame.image.load('p1crab.png')
		self.player = pygame.transform.scale(self.player,(WSCALED,HSCALED))
		self.surf = pygame.Surface((WSCALED, HSCALED),SRCALPHA)
		self.surf.blit(self.player,(0,0))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((WIDTH/2, HEIGHT * 0.89 + HSCALED))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.hp = 0
		self.active = False
	def moveplayer1(self,pewpewpew):
		self.acc = vec(0,0)
		global timelastfireforplayer2
		pressed_keys = pygame.key.get_pressed()
		if self.active == True:            
			if pressed_keys[K_q and K_a]:
				self.acc.x = -ACC
			if pressed_keys[K_d]:
				self.acc.x = ACC
			if pressed_keys[K_w and K_z]:
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
 
#	def hitplayer(self,sp,bul): 
#		for x in bul:
#			col =  pygame.sprite.collide_mask(sp,x)
#			print(col)

class Player2(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__() 
		player = pygame.image.load('p2crab.png')
		player = pygame.transform.scale(player,(WSCALED,HSCALED))
		self.surf = pygame.Surface((WSCALED, HSCALED),SRCALPHA)
		self.surf.blit(player,(0,0))
		self.rect = self.surf.get_rect()
   
		self.pos = vec((WIDTH/2, HEIGHT * 0.11))
		self.vel = vec(0,0)
		self.acc = vec(0,0)
		self.hp = 0
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
					#pewpewpew.append(shootsprite(self.pos,True))

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
			#mypos[0]=mypos[0]-(36/2)
			poss = tuple(mypos)
			self.poss = poss
			self.bullet = pygame.image.load('projectiel2.png')
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
				self.bullet = pygame.image.load('projectiel1.png')
				self.bullet = pygame.transform.scale(self.bullet,(BXSCALE,BYSCALE))

				self.surf = pygame.Surface((WIDTH,HEIGHT),SRCALPHA)#36,27
				self.surf.blit(self.bullet,poss)
				self.rect = self.surf.get_rect() 

def checkplayerhit(player,list):
	for bullet in list:
		global timeLasthit
		bulletposx = round(bullet.poss[0],0)
		bulletposy = round(bullet.poss[1],0)

		playerposx = round(player.pos[0],0)
		playerposy = round(player.pos[1],0)

		left = (playerposx -(WSCALED/2))
		top = (playerposy -(HSCALED))
		right = left + WSCALED
		bottem = top + HSCALED

		bulletLeft = (bulletposx)
		bulletRight = bulletLeft+BXSCALE
		bulletTop = (bulletposy)
		bulletBottem = bulletTop + BYSCALE
		if time.perf_counter()-timeLasthit>0.5:
			if(left<=bulletLeft<=right or left<=bulletRight<=right):
				if(top<=bulletBottem<=bottem or top <bulletTop <=bottem):
					timeLasthit = time.perf_counter()
					return True
	return False

def hit1(p):
	p.hp += 1
	while p.hp == 13:
		return True
	return False

def start(): # 3,2,1 afbeeldingen laten zien en dan movement/schieten unlocken
	global timecdstart 
	if time.time() - timecdstart < 1:
		displaysurface.blit(pygame.transform.scale(cd3,(CDSCALEW,CDSCALEH)),(displaysurface.get_rect().centerx-CDSCALEW//2,displaysurface.get_rect().centery-CDSCALEH//2))
	elif time.time() - timecdstart > 1 and time.time() - timecdstart < 2:
		displaysurface.blit(pygame.transform.scale(cd2,(CDSCALEW,CDSCALEH)),(displaysurface.get_rect().centerx-CDSCALEW//2,displaysurface.get_rect().centery-CDSCALEH//2))
	elif time.time() - timecdstart > 2 and time.time() - timecdstart < 3:
		displaysurface.blit(pygame.transform.scale(cd1,(CDSCALEW,CDSCALEH)),(displaysurface.get_rect().centerx-CDSCALEW//2,displaysurface.get_rect().centery-CDSCALEH//2))
	else:
		P1.active = True
		P2.active = True

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
remove =[]
timecdstart = time.time()
timeLasthit= 0

while True:
	displaysurface.fill((255,255,255))
	displaysurface.blit(pygame.transform.scale(bg,(displaysurface.get_size())),(0,0))	
	displaysurface.blit(pygame.transform.scale(HPplayer1,(HPSCALEDW,HPSCALEDH)), (displaysurface.get_rect().centerx-HPSCALEDW/2,0))
	displaysurface.blit(pygame.transform.scale(HPplayer2,(HPSCALEDW,HPSCALEDH)), (displaysurface.get_rect().centerx-HPSCALEDW/2,HEIGHT- HPSCALEDH))
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
 
	P1.moveplayer1(pewpewpew)
	P2.moveplayer2(pewpewpew)
	playerposx = round(P1.pos[0],0)
	playerposy = round(P1.pos[1],0)

	for pew in pewpewpew:
		bulletposx = round(pew.poss[0],0)
		bulletposy = round(pew.poss[1],0)
		bulletLeft = (bulletposx)
		bulletRight = bulletLeft+BXSCALE
		bulletTop = (bulletposy)
		bulletBottem = bulletTop + BYSCALE

	#P1.hitplayer(P1,pewpewpew)
	## hit player check
	if checkplayerhit(P2,pewpewpew):
		hit1(P2)
	if checkplayerhit(P1,pewpewpew):
		hit1(P1)
	for i in range(0,P1.hp):
		displaysurface.blit(pygame.transform.scale(HPn2,(REDSCALEW+1,REDSCALEH)), (WIDTH*0.645-i*REDSCALEW, HEIGHT*0.9575))
	for i in range(0,P2.hp):
		displaysurface.blit(pygame.transform.scale(HPn,(REDSCALEW+1,REDSCALEH)),(WIDTH*0.3325+i*REDSCALEW,HEIGHT*0.00625))

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
	
