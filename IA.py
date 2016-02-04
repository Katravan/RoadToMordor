import random
import os
import pygame
import grille_classe
import joueur_classe
import unite_classe
import batiment_classe

CONST_BACK_VIDE = 0
CONST_BACK_FLEUR = 1
CONST_BACK_OBS_VIDE = 2
CONST_BACK_OBS_LAVA = 3

CONST_FRONT_VIDE = 0
CONST_FRONT_ROUTE = 1
CONST_FRONT_FORET = 2
CONST_FRONT_ROCHER = 3
CONST_FRONT_BUCHES = 4
CONST_FRONT_TRONC = 5

CONST_FRONT_BAT = 9

CONST_UNIT_VIDE = 0
CONST_UNIT_USED = 1


class IA:

	def __init__(self,grille,joueur):
		self.joueur = joueur
		self.grille = grille.getGrille()
		self.grille_obj = grille
		self.routes = self.grille_obj.routes

	def play(self):
		#print("===================================\nArgent IA ava,t tour = {}".format(self.joueur.getArgent()))
		self.tour_IA()
		#print("Argent IA apres tour = {}\n===================================".format(self.joueur.getArgent()))

	def get_IA_soldat_route(self,nb_route):
		IA = []
		route = self.routes[nb_route]
		i  = 0
		while i <= len(route)-1:
			if self.grille[route[i]["x"]][route[i]["y"]]["unit"] == CONST_UNIT_USED:
				if self.grille[route[i]["x"]][route[i]["y"]]["item"].getEquipe() == 0:
					IA.append(self.grille[route[i]["x"]][route[i]["y"]]["item"])
			i+=1
		return IA

	def get_humain_soldat_route(self,nb_route):
		humain = []
		route = self.routes[nb_route]
		i  = 0
		while i <= len(route)-1:
			if self.grille[route[i]["x"]][route[i]["y"]]["unit"] == CONST_UNIT_USED:
				if self.grille[route[i]["x"]][route[i]["y"]]["item"].getEquipe() == 1:
					humain.append(self.grille[route[i]["x"]][route[i]["y"]]["item"])
			i+=1
		return humain

	def get_humain_tour_route(self,nb_route):
		tours = []
		coord = []
		route = self.routes[nb_route]
		i  = 0
		while i <= len(route)-1:
			x = route[i]["x"]
			y = route[i]["y"]
			j = x-1
			k = y-1
			while (j <= x + 1):
				k = y - 1
				while (k <= y + 1):
					try:
						if self.grille[j][k]['front'] == CONST_FRONT_BAT:
							if self.grille[j][k]['item'].getEquipe() == 1 and [j,k] not in coord:
								t = self.grille[j][k]['item']
								tours.append(t)
								coord.append([t.getPos["x"],t.getPos["y"]])
					except IndexError:
						continue
					finally:
						k+=1
				j+=1


			i+=1
		return tours

	def get_IA_tour_route(self,nb_route):
		tours = []
		coord = []
		route = self.routes[nb_route]
		i  = 0
		while i <= len(route)-1:
			x = route[i]["x"]
			y = route[i]["y"]
			j = x-1
			k = y-1
			while (j <= x + 1):
				k = y - 1
				while (k <= y + 1):
					try:
						if self.grille[j][k]['front'] == CONST_FRONT_BAT:
							if self.grille[j][k]['item'].getEquipe() == 0 and [j,k] not in coord:
								t = self.grille[j][k]['item']
								tours.append(t)
								coord.append([t.getPos()["x"],t.getPos()["y"]])
					except IndexError:
						continue
					finally:
						k+=1
				j+=1


			i+=1
		return tours

	def nb_route_autour(self,radius,x,y):
		nb = 0
		i = x - radius
		while (i <= x + radius):
			j = y - radius
			while (j <= y + radius):
				try:
					if self.grille[i][j]['front'] == CONST_FRONT_ROUTE:
						nb+=1
				except IndexError:
					continue
				finally:
					j+=1
			i+=1
		return nb


	def generer_tour(self,choix_route,choix_tour):
		temp_i, temp_j, max1, nbcase = 0,0,0,0
		nb_route = (len(self.routes)+1)
		if self.grille_obj.rows%nb_route != 0:
			s = self.grille_obj.rows-((self.grille_obj.rows/len(self.grille))+(self.grille_obj.rows%len(self.grille)))
			f = self.grille_obj.rows
		else:
			s = (self.grille_obj.rows/nb_route)*choix_route
			f = (self.grille_obj.rows/nb_route)*(choix_route+1)-1

		for i in range((len(self.grille)/2)+1,len(self.grille)):
			for j in range(s,f):
				if self.grille[i][j]['front'] == CONST_FRONT_VIDE:
					nbcase = self.nb_route_autour(1,i,j)
					if (nbcase > max1):
						max1 = nbcase
						temp_i = i
						temp_j = j
		"""
		bat = batiment_classe.Batiment(choix_tour,0,"Tour IA",self.grille_obj,{'x':temp_i,'y':temp_j})
		self.grille_obj.place(bat)
		self.joueur.payerArgent(bat.getPrix())
		"""
		if self.grille_obj.canBuild({'x':temp_i,'y':temp_j},self.joueur.getEquipe()):
			tour = self.joueur.createBuild(choix_tour,self.grille_obj,{'x':temp_i,'y':temp_j})
			print('TOUR a {},{}'.format(temp_i,temp_j),'front : ',self.grille[temp_i][temp_j]['front'])
			if not tour == False:
				self.grille_obj.place(tour)
				print("==================================== TOUR Genere")
		# Faire payer l'IA
		#joueur.payer(self.grille[temp_i][temp_j]['batiment'].getPrix())

	def generer_homme(self,choix_route,choix_unit):
		"""
		unit = unite_classe.Unite(choix_unit,"guignol IA",0,self.grille_obj,self.routes[choix_route],choix_route)
		self.grille_obj.place(unit)
		self.joueur.payerArgent(unit.getPrix())
		"""
		print("==================================== SOLDAT Genere")
		homme = self.joueur.createUnit(choix_unit,self.grille_obj,self.routes[choix_route])
		if not homme == False:
			self.grille_obj.place(homme)

	def stats_joueurs_route(self,nb_route):
		allies = self.get_humain_soldat_route(nb_route)
		ennemis = self.get_IA_soldat_route(nb_route)
		route = self.grille[nb_route]
		attaquePhy = 0
		attaqueMag = 0
		defensePhy = 0
		defenseMag = 0
		totalVie = 0
		stats = []
		stats.append([])
		for unit in ennemis:
			totalVie+=unit.getVie()
			attaquePhy+=unit.getAttPhy()
			attaqueMag+=unit.getAttMag()
			defensePhy+=unit.getResPhy()
			defenseMag+=unit.getResMag()
		stats[0].append(totalVie)
		stats[0].append(attaquePhy)
		stats[0].append(attaqueMag)
		stats[0].append(defensePhy)
		stats[0].append(defenseMag)

		stats.append([])
		attaquePhy = 0
		attaqueMag = 0
		defensePhy = 0
		defenseMag = 0
		totalVie = 0
		for unit in allies:
			totalVie+=unit.getVie()
			attaquePhy+=unit.getAttPhy()
			attaqueMag+=unit.getAttMag()
			defensePhy+=unit.getResPhy()
			defenseMag+=unit.getResMag()
		stats[1].append(totalVie)
		stats[1].append(attaquePhy)
		stats[1].append(attaqueMag)
		stats[1].append(defensePhy)
		stats[1].append(defenseMag)
		return stats

	def stats_tour_route(self,nb_route):
		allies = self.get_humain_tour_route(nb_route)
		ennemis = self.get_IA_tour_route(nb_route)
		route = self.grille[nb_route]
		attaquePhy=0
		attaqueMag=0
		stats = []
		stats.append([])
		for unit in ennemis:
			attaquePhy+=unit.getAttPhy()
			attaqueMag+=unit.getAttMag()
		stats[0].append(attaquePhy)
		stats[0].append(attaqueMag)

		stats.append([])
		attaquePhy=0
		attaqueMag=0
		for unit in allies:
			attaquePhy+=unit.getAttPhy()
			attaqueMag+=unit.getAttMag()
		stats[1].append(attaquePhy)
		stats[1].append(attaqueMag)
		return stats


	def tour_IA(self):
		argent = self.joueur.getArgent()
		if argent >=5:
			calcul_units = []
			calcul_tours = []
			nb_routes = len(self.routes)
			for i in range(nb_routes):
				calcul_units.append(self.stats_joueurs_route(i))
			for i in range(nb_routes):
				calcul_tours.append(self.stats_tour_route(i))


			#L'IA essaye de contrer d'abord les attaques
			for i in range(nb_routes):
				if calcul_units[i][1][0] >= calcul_tours[i][0][0]*2+calcul_tours[i][0][1]*2+calcul_units[i][0][1]+calcul_units[i][0][2]:
					#envoyer unit ou construire tours
					alea = random.randrange(5)
					if alea !=0:
						print("BAT PREMIERE PHASE")
						while self.joueur.getArgent() > (argent/4)*3 and self.stats_joueurs_route(i)[1][0] >= self.stats_tour_route(i)[0][0]*2+self.stats_tour_route(i)[0][1]+self.stats_joueurs_route(i)[0][1]+self.stats_joueurs_route(i)[0][2]:
							print("== While 1, ArgentJoueur = {},(argent/4)*3 = {}".format(self.joueur.getArgent(),(argent/4)*3))
							alea2 = random.randrange(20)
							if alea2 >=9 :
								self.generer_tour(i,0)
							elif alea2 <9 and alea2 >= 3:
								self.generer_tour(i,1)
							elif alea2 <3 :
								self.generer_tour(i,2)
					else:
						print("SOL PREMIERE PHASE")
						while self.joueur.getArgent() > (argent/4)*2 and self.stats_joueurs_route(i)[1][0] >= self.stats_tour_route(i)[0][0]*2+self.stats_tour_route(i)[0][1]+self.stats_joueurs_route(i)[0][1]+self.stats_joueurs_route(i)[0][2]:
							print("== While 2")
							alea2 = random.randrange(20)
							if alea2 >=9 :
								print("SOLDAT GENERE PAR PREMIERE PHASE")
								self.generer_homme(i,0)
							elif alea2 <9 and alea2 >= 3:
								print("SOLDAT GENERE PAR PREMIERE PHASE")
								self.generer_homme(i,1)
							elif alea2 <3 :
								print("SOLDAT GENERE PAR PREMIERE PHASE")
								self.generer_homme(i,2)

			#Puis avec les ressources qui lui reste elle attaque
			min_vie = 150000
			min_tours = 150000
			choix_attaque_unit = -1
			choix_attaque_tour = -1

			for i in range(nb_routes):
				if min_vie != min(min_vie,calcul_units[i][1][0]):
					min_vie = min(min_vie,calcul_units[i][1][0])
					choix_attaque_unit = i
				if min_tours != min(min_tours,calcul_tours[i][1][0]+calcul_tours[i][1][1]):
					min_tours = min(min_tours,calcul_tours[i][1][0]+calcul_tours[i][1][1])
					choix_attaque_tour = i

			if choix_attaque_unit == choix_attaque_tour:
				while self.joueur.getArgent() > (argent/10):
					alea2 = random.randrange(20)
					if alea2 >=9 :
						print("SOLDAT GENERE PAR SECONDE PHASE")
						self.generer_homme(choix_attaque_tour,0)
					elif alea2 <9 and alea2 >= 3:
						print("SOLDAT GENERE PAR SECONDE PHASE")
						self.generer_homme(choix_attaque_tour,1)
					elif alea2 <3 :
						print("SOLDAT GENERE PAR SECONDE PHASE")
						self.generer_homme(choix_attaque_tour,2)
			else :
				while self.joueur.getArgent() > argent/10:
					alea2 = random.randrange(20)
					if alea2 >=9 :
						print("SOLDAT GENERE PAR SECONDE PHASE")
						self.generer_homme(choix_attaque_tour,0)
					elif alea2 <9 and alea2 >= 3:
						print("SOLDAT GENERE PAR SECONDE PHASE")
						self.generer_homme(choix_attaque_tour,1)
					elif alea2 <3 :
						print("SOLDAT GENERE PAR SECONDE PHASE")
						self.generer_homme(choix_attaque_tour,2)


	"""def tour_IA(self,grille):
		alea = random.randrange(100)
		if(Grille.nb_tour <= 5):
			if (alea < 50):
				Grille.generer_homme()
			else:
				Grille.generer_tour()
		if(Grille.nb_tour <	= 10 and Grille.nb_tour > 5 ):
			if (alea < 60):
				Grille.generer_homme()
			elif( alea > 89 ):
				Grille.generer_upgrade()
			else:
				Grille.generer_tour()
		if(Grille.nb_tour <= 15 and Grille.nb_tour > 10 ):
			if (alea < 60):
				Grille.generer_homme()
			elif( alea > 79 ):
				Grille.generer_upgrade()
			else:
				Grille.generer_tour
		if(Grille.nb_tour <= 25 and Grille.nb_tour > 15 ):
			if (alea < 70):
				Grille.generer_homme()
			elif( alea > 79 ):
				Grille.generer_upgrade()
			else:
				Grille.generer_tour
		if(Grille.nb_tour > 25 ):
			if (alea < 60):
				Grille.generer_homme()
			else:
				Grille.generer_upgrade()"""
