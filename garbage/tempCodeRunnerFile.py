		
			if time.time()-timelastfireforplayer2>0.05:
				timelastfireforplayer2 = time.time()
				updateposbulletlist=list(self.pos)
				updateposbulletlist[0]=updateposbulletlist[0]-(BXSCALE/2)
				updateposbulletlist=tuple(updateposbulletlist)
				pewpewpew.append(shootsprite(updateposbulletlist,False))