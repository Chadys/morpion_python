import pdb

# Coder un joueur intelligent de morpion en python
#	Minimax, profondeur (par defaut) n=3
#	les deux heuristiques : h1(p)=nbAlignements(p,x)-nbAlignements(p,o)
#							h2(p)=(3*nbAlignements2(p,x)+nbAlignements1(p,x))-(3*nbAlignements2(p,o)+nbAlignements1(p,o))
#								nbAlignements i(p,j) = nombre d'alignements realisables par le joueur j pour lesquels il a deja i symboles en place
#	par defaut le joueur humain joue en second

#	Options :
#		profondeur n passee en parametre
#		ordre des joueurs passe en parametre
#		elagage alpha-beta
#		proposition d'autres heuristiques

# Rappels : ordre d'examen des successeurs directs, ordre des colonnes d'abord, des lignes ensuite
# 1|4|7
# 2|5|8		-X 1er joueur MAX
# 3|6|9		-O 2nd joueur MIN

L = ([[0,0,0],[0,0,0],[0,0,0]]) # Grille vide de depart


def affiche () :
	print "  1  2  3"
	x = 1
	for i in L :
		print x,
		for j in i :
			if(j==0) :
				print "_|",
			if(j==1) :
				print "X|",
			if(j==2) :
				print "O|",
		x+=1
		print
# Affiche ceci :
#  1 2 3
#1 _|_|_|
#2 _|_|_|
#3 _|_|_| ou chaque _ sera remplacer par un X ou un O en fonction de la liste


def demarre () :
	print "Bienvenue sur le jeu du Morpion !"
	print
	try:
		mode = input("Voulez-vous jouer au mode JvsJ, IAvsJ ou IAvsIA ? Taper 1, 2 ou 3 : ")
	except (NameError, TypeError, SyntaxError):
		print "Entree invalide, priere de recommencer"
		print
		demarre()
	else :
		if (mode not in [1,2,3]) :
			print "Entree invalide, priere de recommencer"
			print
			demarre()

		if (mode==1) : #JvsJ
			affiche()
			print
			x=0
			while (0 in L[0] or 0 in L[1] or 0 in L[2]) :
				print "Tour du joueur " + str(x+1) + " :"
				j = jouejoueur(x+1)
				affiche()
				print
				a=j[0]
				b=j[1]
				if (victoire(a,b,x+1,L)) : # verifie si le dernier mouvement cause une victoire
					print "Le joueur " + str(x+1) + " a gagne, felicitation !"
					return
				x = x ^ 1
			print "Egalite, dommage !"
		#lance une partie joueur versus joueur, echange le numero du joueur a chaque boucle
		#s'arrete si grille pleine ou victoire

		if (mode==2) : # JvsIA
			try:
				y= input("Voulez vous jouer contre l'IA minimax ou alphabeta ? tapez 1 ou 2 : ")
				n = input("Choisissez la profondeur evaluee par l'IA entre 1 et 9 : ")
				h = input("Choisissez l'heuristique utilisee par l'IA entre 1 et 3 : ")
				j = input("Voulez-vous jouer en premier ou en deuxieme ? tapez 1 ou 2 : ")
			except (NameError, TypeError, SyntaxError):
				print "Entree invalide, priere de recommencer"
				print
				demarre()
			else :
				if (y not in (1,2) or n not in xrange(1,10) or h not in [1,2,3] or j not in (1,2)) :
					print "Entree invalide, priere de recommencer"
					print
					demarre()
				affiche()
				print
				x=j-1 # variable qui indique c'est au tour de qui, si 0 tour joueur si 1 tour ordi
				m=(x^1)+1 # numero de joueur de l'IA
				while (0 in L[0] or 0 in L[1] or 0 in L[2]) :
					if (x) :
						print "Tour de l'ordinateur :"
						i = ia(n,m,y,h)
						affiche()
						print
						a=i[0]
						b=i[1]
						if (victoire(a,b,m,L)) :
							print "L'ordinateur a gagne, dommage !"
							return
					else :
						i = jouejoueur(j)
						affiche()
						print
						a=i[0]
						b=i[1]
						if (victoire(a,b,j,L)) :
							print "Vous avez gagne, felicitation !"
							return
					x = x ^ 1
				print "Egalite, dommage !"
		#lance une partie joueur versus ordinateur demarre selon que le joueur commence ou non puis echange
		#IA minimax ou alphabeta avec profondeur et heuristique au choix, s'arrete si grille pleine ou victoire
		
		if (mode == 3) : # IAvsIA
			try:
				n1 = input("Choisissez la profondeur evaluee par l'IA minimax entre 1 et 9 : ")
				n2 = input("Choisissez la profondeur evaluee par l'IA alphabeta entre 1 et 9 : ")
				h1 = input("Choisissez l'heuristique utilisee par l'IA minimax entre 1 et 3 : ")
				h2 = input("Choisissez l'heuristique utilisee par l'IA alphabeta entre 1 et 3 : ")
				j = input("Voulez-vous que l'IA minimax joue en premier ou en deuxieme ? tapez 1 ou 2 : ")
			except (NameError, TypeError, SyntaxError):
				print "Entree invalide, priere de recommencer"
				print
				demarre()
			else :
				if (n1 not in xrange(1,10) or n2 not in xrange(1,10) or h1 not in [1,2,3] or h2 not in [1,2,3] or j not in (1,2)) :
					print "Entree invalide, priere de recommencer"
					print
					demarre()
				affiche()
				print
				x=j-1 # si 1 tour minimax sinon tour alphabeta
				m=(x^1)+1 # numero joueur alphabeta
				while (0 in L[0] or 0 in L[1] or 0 in L[2]) :
					if (x) :
						i=ia(n2,m,2,h2)
						print "Tour de l'ordinateur alphabeta :"
						affiche()
						print
						a=i[0]
						b=i[1]
						if (victoire(a,b,m,L)) :
							print "L'ordinateur alphabeta a gagne !"
							return
						try :
							input("Appuyez sur Entree...")
						except (NameError, TypeError, SyntaxError):
							pass
					else :
						i=ia(n1,j,1,h1)
						print "Tour de l'ordinateur minimax :"
						affiche()
						print
						a=i[0]
						b=i[1]
						if (victoire(a,b,j,L)) :
							print "L'ordinateur minimax a gagne !"
							return
						try :
							input("Appuyez sur Entree...")
						except (NameError, TypeError, SyntaxError):
							pass
					x = x ^ 1
				print "Egalite, dommage !"
		#lance une partie ordinateur versus ordinateur avec les preferences au choix


def jouejoueur (i) :
	try:
		x = input("Sur quelle ligne voulez vous jouer ? ")-1
		y = input("Sur quelle colonne voulez vous jouer ? ")-1
	except (NameError, TypeError, SyntaxError):
		print "Entree invalide, priere de recommencer"
		print
		return jouejoueur(i)
	else:
		if (x not in [0,1,2] or y not in [0,1,2]) :
			print "Entree invalide, priere de recommencer"
			print
			return jouejoueur(i)
		else :
			if (L[x][y]!=0) :
				print "Case deja utilisee, priere de recommencer"
				print
				return jouejoueur(i)
			else :
				L[x][y] = i
				return [x,y]
# Modifie la grille en fonction du coup joue, renvoie la position jouee


def victoire(a,b,j,l) :
	x,y = 0,0
	#test ligne et colonne correspondantes
	for k in xrange(3) :
		if (k!=b and l[a][k]==j) :
			x+=1
		if (x == 2) :
			return True
		if (k!=a and l[k][b]==j) :
			y+=1
		if (y == 2) :
			return True
	#test diagonale 1 si besoin
	x,y = 0,0
	if(a == b) :
		for k in xrange(3) :
			if (k!=a and l[k][k]==j) :
				x+=1
			if(x == 2) :
				return True
	#test diagonale 2 si besoin
	if(a+b == 2) :
		for k in xrange(3) :
			for x in xrange(3) :
				if(k+x==2 and k!=a and l[k][x]==j) :
					y+=1
				if (y == 2) :
					return True
	return False
# Test de victoire, renvoie 1 si dernier joueur gagnant, sinon 0
# Ne verifie que les cases necessaires en fonction du dernier coup joue
	

def parcours(l) :
	l1,l2,l3, c1,c2,c3, d1,d2, npions = 0,0,0, 0,0,0, 0,0, 0
	if (l[0][0] == 1) :
		npions+=1
		l1+=1
		c1+=1
		d1+=1
	if (l[0][0] == 2) :	
		npions+=1	
		l1+=10
		c1+=10
		d1+=10
	if (l[0][1] == 1) :
		npions+=1
		l1+=1
		c2+=1
	if (l[0][1] == 2) :		
		npions+=1
		l1+=10
		c2+=10
	if (l[0][2] == 1) :
		npions+=1
		l1+=1
		c3+=1
		d2+=1
	if (l[0][2] == 2) :		
		npions+=1
		l1+=10
		c3+=10
		d2+=10
	if (l[1][0] == 1) :
		npions+=1
		l2+=1
		c1+=1
	if (l[1][0] == 2) :		
		npions+=1
		l2+=10
		c1+=10
	if (l[1][1] == 1) :
		npions+=1
		l2+=1
		c2+=1
		d1+=1
		d2+=1
	if (l[1][1] == 2) :		
		npions+=1
		l2+=10
		c2+=10
		d1+=10
		d2+=10
	if (l[1][2] == 1) :
		npions+=1
		l2+=1
		c3+=1		
	if (l[1][2] == 2) :		
		npions+=1
		l2+=10
		c3+=10
	if (l[2][0] == 1) :
		npions+=1
		l3+=1
		c1+=1
		d2+=1
	if (l[2][0] == 2) :		
		npions+=1
		l3+=10
		c1+=10
		d2+=10
	if (l[2][1] == 1) :
		npions+=1
		l3+=1
		c2+=1
	if (l[2][1] == 2) :		
		npions+=1
		l3+=10
		c2+=10
	if (l[2][2] == 1) :
		npions+=1
		l3+=1
		c3+=1
		d1+=1
	if (l[2][2] == 2) :	
		npions+=1	
		l3+=10
		c3+=10
		d1+=10
	return [l1,l2,l3,c1,c2,c3,d1,d2,npions]
# Parcours de la grille, renvoie une liste de variables pour chaque ligne, colonne, diagonale et le nombre de pions
# utile pour les heuristiques

def h1(l) :
	h=0
	H = parcours(l)
	H.pop()
	for i in H :
		if (i == 3) :
			return 100
		if (i == 30) :
			return -100
		if i in (0,1,2) :
			h+=1
		if (i%10 == 0) :
			h-=1
	return h
# Test de la premiere heuristique, utilise parcours() sans le nombre de pions
# Fait le calcul a partir de chaque variable ou renvoie 100 si victoire X, -100 si victoire O

def h2(l) :
	h=0
	H = parcours(l)
	H.pop()
	for i in H :
		if (i == 3) :
			return 100
		if (i == 30) :
			return -100
		if (i == 1) :
			h+=1
		if (i == 2) :
			h+=3
		if (i == 10) :
			h-=1
		if (i == 20) :
			h-=3
	return h
# Test de la deuxieme heuristique, fonctionnement semblable a la premiere, seuls les quotients changent

def h3(l) :
	h=0
	H = parcours(l)
	npions=H.pop()
	for i in H :
		if (i == 3) :
			return 100-npions
		if (i == 30) :
			return (-100)+npions
		if (i == 1) :
			h+=1
		if (i == 2) :
			h+=3
		if (i == 10) :
			h-=1
		if (i == 20) :
			h-=3
	return h
# Troisieme heuristique qui fonctionne presque comme la deuxieme
# en cas de victoire, ajout ou retrait du nombre de pions pour qu'elle n'est pas la meme valeur selon qu'elle soit atteignable plus ou moins rapidement
# permet a l'IA de favoriser la victoire la plus rapide ou la defaite la plus lente selon le cas


def ia(n, m, i, h) :
	if (i==1) :
		l=minimax(n,m,h)
	if (i==2) :
		if (h==3) :
			l=alphabeta(n,m,-94,95,h) # avec l'heuristique 3 les minimum et maximum atteignables ne sont plus les memes
		else :
			l=alphabeta(n,m,-100,100,h)
	L[l[1]][l[2]]=m
	return l[1:]
# IA, joue le coup le plus prometteur en fonction de l'evaluation de minimax ou alphabeta avec l'heuristique indiquee, renvoie le coup joue

def minimax(n,m,h, l=L) : # n=profondeur, m=joueur min(2) ou max(1), h=heuristique utilisee, l=liste test (grille du jeu en cours par defaut)
	M=[] # liste de l'evaluation du meilleur coup et les positions pour l'atteindre
	for i in xrange(3) :
		for j in xrange(3) :
			if(l[j][i] == 0) :
				l[j][i]=m
				if(n==0 or victoire(j,i,m,l) or not(0 in l[0] or 0 in l[1] or 0 in l[2])) : #evaluation de la position si terminale ou profondeur atteinte
					if (h==1):
						temp=h1(l)
					if (h==2):
						temp=h2(l)
					if(h==3):
						temp=h3(l)
					if((not M) or (m==2 and temp<M[0]) or (m==1 and temp>M[0])) :
						M=[temp,j,i] #si liste vide ou evaluation meilleure, la liste devient ce coup
				else :
					temp=minimax(n-1,(((m-1)^1)+1),h,l) # recursivite avec la grille modifiee en baissant la profondeur et echangeant le joueur min/max
					if((not M) or (m==2 and temp[0]<M[0]) or (m==1 and temp[0]>M[0])) :
						M=[temp[0],j,i] #si liste vide ou evaluation des successeurs meilleure, la liste devient ce coup
				l[j][i]=0
	return M
# Retourne le meilleur coup a jouer et son evaluation en allant a une profondeur max n et en utilisant l'heuristique h


def alphabeta(n,m,alpha,beta,h, l=L) : # alpha = evaluation minimum, beta=evalution maximum
	M=[] # liste de l'evaluation du meilleur coup et les positions pour l'atteindre
	for i in xrange(3) :
		for j in xrange(3) :
			if(l[j][i] == 0) :
				l[j][i]=m
				if(n==0 or victoire(j,i,m,l) or not(0 in l[0] or 0 in l[1] or 0 in l[2])) : #evaluation de la position si terminale ou profondeur atteinte
					if (h==1):
						temp=h1(l)
					if(h==2):
						temp=h2(l)
					if(h==3):
						temp=h3(l)
					if((not M) or (m==2 and temp<M[0]) or (m==1 and temp>M[0])) :
						M=[temp,j,i]
				else :
					if(m==2) :
						temp=alphabeta(n-1,(((m-1)^1)+1),alpha,beta,h,l)
						if((not M) or temp[0]<M[0]) :
							M=[temp[0],j,i]
						if(temp[0]<beta) :
							beta=temp[0]
						if (temp[0] <= alpha) : #coupure alpha
							l[j][i]=0
							break
					else :
						temp=alphabeta(n-1,(((m-1)^1)+1),alpha,beta,h,l)
						if((not M) or temp[0]>M[0]) :
							M=[temp[0],j,i]
						if(temp[0]>alpha) :
							alpha=temp[0]
						if (temp[0] >= beta) : #coupure beta
							l[j][i]=0
							break
				l[j][i]=0
		else:
			continue #si la boucle interieure se finit normalement, continue la boucle exterieure
		break #casse la boucle exterieure si la boucle interieure a eu une coupure
	return M
# Retourne le meilleur coup a jouer en sautant les evaluations inutiles


demarre()