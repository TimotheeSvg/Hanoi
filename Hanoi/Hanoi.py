from tkinter import * 
import random

#parametres fenetre et affichage
H_SIZE = 720
W_SIZE = 1080
NBR_PIECE = 8


TITLE = "Hanoî" 
BACKGROUND_COLOR = "#CBDBF2"

#plateau
COULEUR_PLATEAU = '#3F3F3F'
OFFSET_Y = H_SIZE *0.9
BORDER_OFFSET = W_SIZE * 0.05
BASE_W = W_SIZE - BORDER_OFFSET 
BASE_H = H_SIZE * 0.05

#tour
COULEUR_TOUR = "#6C6C73"
BASE_BORDER_OFFSET = BASE_W * 0.1
PILLIER_H = H_SIZE * 0.55
PILLIER_W = W_SIZE * 0.03
BORDER_TOP = (H_SIZE- OFFSET_Y) 
#offset des différentes tours
POSITION = [
    BORDER_OFFSET + BASE_BORDER_OFFSET,
    W_SIZE//2,
    W_SIZE - BORDER_OFFSET - BASE_BORDER_OFFSET
    ]

#piece
PIECE_H = PILLIER_H * 0.9 // NBR_PIECE - PILLIER_H*0.5//NBR_PIECE
PIECE_COULEUR = [["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])] for _ in range(NBR_PIECE)]
PIECE_W = []

ecart = (POSITION[1]-POSITION[0])
for i in range(NBR_PIECE):
    PIECE_W.append(ecart - ((W_SIZE//20)*i))

#taux de rafraichissement
TIMEDELAY = 1
#vitesse des blocs
STEP = 1

class Plateau:
    def __init__(self):
        self.canvas = Canvas(window, width=W_SIZE, height=H_SIZE, background=BACKGROUND_COLOR)
        
        #compteur de déplacement pour 1 Bloc (0 = monter, 1 = direction latéral, 2 = descendre)
        self.cmptMovDessin = 0

        #compteur d'étapes effectuées
        self.cmptMovStrategie = 0
        
        #Creation socle                                                                                     
        self.canvas.create_rectangle(BORDER_OFFSET,OFFSET_Y, BASE_W ,OFFSET_Y+ BASE_H, fill=COULEUR_PLATEAU, outline="")

        #Creation tour
        for i in range(3):
            self.canvas.create_rectangle(POSITION[i] ,OFFSET_Y, POSITION[i] + PILLIER_W ,OFFSET_Y-PILLIER_H, fill=COULEUR_TOUR, outline="")
      

        
        #creation Piece
        self.piece = []
        for i in range(NBR_PIECE):
            #offset des positions celon les coordonées de POSITION et la largeur des disques celon PIECE_W
            x0 = POSITION[0] - PIECE_W[i] //2 + PILLIER_W//2
            y0 = OFFSET_Y - i*PIECE_H
            x1 = x0 + PIECE_W[i]
            y1 =(OFFSET_Y - i*PIECE_H)- PIECE_H
            
            #création des rectangles celon les offsets
            self.piece.append(self.canvas.create_rectangle( x0,y0, x1 ,y1, fill=PIECE_COULEUR[i], outline=""))
              
        #0 = Grande 3 = Petite
        #initialisation des pièces sur la tour 0
        self.tabPiecePosition = [0 for _ in range(NBR_PIECE)]
        

        #initialisation de la stratégie
        self.strategie = []

        #ajout des mouvement aller (calculMouvement, 0:Start, 0:Tour source, 1: Tour Auxiliaire, 2: Tour visée)
        self.calculMouvement(0,0,1,2)

        #ajout des mouvement retour (calculMouvement, 0:Start, 2:Tour source, 1: Tour Auxiliaire, 0: Tour visée)
        self.calculMouvement(0,2,1,0)

        self.canvas.pack()

    #start : compteur partant de 0 allant jusqu'au nombre de disque - 1 (3 pour l'exercice)
    #source : id de la tour ayant tout les disques au début 
    #auxiliaire : id de la tour permettant les rotations 
    #destination : id de la tour visée 
          
    def calculMouvement(self, start,source, auxiliaire,destination):
        #Début de la stratégie par récursivité

        #demande d'arret = nbr de disque - 1
        if start==NBR_PIECE - 1:
            self.strategie.append([start, destination])
            return
        #appel récursif visant a deplacer la pièces de source sur la tour auxiliaire
        self.calculMouvement(start+1, source, destination, auxiliaire)  
        self.strategie.append([start, destination])
        #appel récursif visant a deplacer la pièces de auxiliaire sur la tour destination
        self.calculMouvement(start+1, auxiliaire, source, destination)
        
    def jouer(self):
        #on demande le mouvement de stratégie celon le n° de movement deja effectué
        self.movement(self.strategie[self.cmptMovStrategie][0],self.strategie[self.cmptMovStrategie][1])
        
        if (self.cmptMovStrategie < len(self.strategie)):
            self.canvas.after(TIMEDELAY,self.jouer)

    def movement(self, piece, pos):
        #On parcour les étapes celon la pièce et la pos demandée

        #etape 0: Monter
        if self.cmptMovDessin == 0:
            self.movementUp(piece)

        #etape 1 : latéral
        elif self.cmptMovDessin == 1:
            if (self.tabPiecePosition[piece] < pos):
                #mouvement vers la droite
                self.movementRight(piece, pos)
            else:
                #mouvement vers la gauche
                self.movementLeft(piece, pos)

        #etape 2 : descendre
        elif self.cmptMovDessin == 2:
            self.movementDown(piece,pos)

        #etape 3 : compter une fin de mouvement
        elif self.cmptMovDessin == 3:
            #set la nouvelle position
            self.tabPiecePosition[piece]  = pos
            #+1 mouvement dans la strategie
            self.cmptMovStrategie +=1
            #reset des étapes d'un dessin
            self.cmptMovDessin =0
        
    def movementUp(self,i):
        #On monte la pièce jusqu'a 150 pixel
        if (self.canvas.coords(self.piece[i])[1] >= BORDER_TOP):
            self.canvas.move(self.piece[i], 0, -STEP)
        else:
            self.cmptMovDessin +=1
    def movementDown(self,i, pos):
        #on descends la piece jusqu'a la hauteur de la base + la hauteur du nombre de bloc présent sur la tour
        if (self.canvas.coords(self.piece[i])[1] <= OFFSET_Y-PIECE_H- self.tabPiecePosition.count(pos)*PIECE_H):
            self.canvas.move(self.piece[i], 0, STEP)
        else:
            self.cmptMovDessin +=1  
    def movementRight(self,i, pos):
        #deplacement vers la droite jusqu'au coordonées de la tour visée
        if(self.canvas.coords(self.piece[i])[0] <= POSITION[pos] - PIECE_W[i] //2 + PILLIER_W//2):
            self.canvas.move(self.piece[i], STEP, 0)  
        else:
            self.cmptMovDessin +=1
    def movementLeft(self,i, pos):
        #deplacement vers la gauche jusqu'au coordonées de la tour visée
        if(self.canvas.coords(self.piece[i])[0] >= POSITION[pos]- PIECE_W[i] //2 + PILLIER_W//2 ):
            self.canvas.move(self.piece[i], -STEP, 0)  
        else:
            self.cmptMovDessin +=1
 
    
        
window = Tk()
window.title(TITLE)
window.geometry(f"{W_SIZE}x{H_SIZE}")
window.resizable(width=0, height=0)

P = Plateau()
P.jouer()

window.mainloop()