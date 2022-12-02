from tkinter import * 

#parametres fenetre et affichage
H_SIZE = 600
W_SIZE = 720

TITLE = "Hanoî" 
BACKGROUND_COLOR = "#CBDBF2"

#plateau
COULEUR_PLATEAU = '#3F3F3F'
OFFSET_Y = H_SIZE *0.7
BORDER_OFFSET = 100
BASE_W = 600
BASE_H = 30

#tour
COULEUR_TOUR = "#6C6C73"
PILLIER_H = 150
PILLIER_W = 20

#piece

PIECE_H = 25
PIECE_W = [113,95,70,45]
PIECE_COULEUR = ['#152A22','#305E4C','#56AE8C','#77FBC8']

#offset des différentes tours
POSITION = [100,350,600]

#taux de rafraichissement
TIMEDELAY = 1

#vitesse des blocs
STEP = 0.31

class Plateau:
    def __init__(self):
        self.canvas = Canvas(window, width=W_SIZE, height=H_SIZE, background=BACKGROUND_COLOR)
        
        #compteur de déplacement pour 1 Bloc (0 = monter, 1 = direction latéral, 2 = descendre)
        self.cmptMovDessin = 0

        #compteur d'étapes effectuées
        self.cmptMovStrategie = 0
        
        #Creation socle                                                                                     
        self.canvas.create_rectangle(BORDER_OFFSET -W_SIZE * 0.04 ,OFFSET_Y, BASE_W + W_SIZE * 0.06,OFFSET_Y+ BASE_H, fill=COULEUR_PLATEAU, outline="")

        #Creation tour
        self.canvas.create_rectangle(100 ,OFFSET_Y, 100 + PILLIER_W ,OFFSET_Y-PILLIER_H, fill=COULEUR_TOUR, outline="")
        self.canvas.create_rectangle(350 ,OFFSET_Y, 350 + PILLIER_W ,OFFSET_Y-PILLIER_H, fill=COULEUR_TOUR, outline="")            
        self.canvas.create_rectangle(600 ,OFFSET_Y, 600 + PILLIER_W ,OFFSET_Y-PILLIER_H, fill=COULEUR_TOUR, outline="")
      
        #creation Piece
        self.piece = []
        for i in range(4):
            #offset des positions celon les coordonées de POSITION et la largeur des disques celon PIECE_W
            x0 = POSITION[0] - PIECE_W[i] +20
            y0 = OFFSET_Y - i*PIECE_H
            x1 = POSITION[0] + PIECE_W[i]
            y1 =(OFFSET_Y - i*PIECE_H)- PIECE_H

            #création des rectangles celon les offsets
            self.piece.append(self.canvas.create_rectangle( x0,y0, x1 ,y1, fill=PIECE_COULEUR[i], outline=""))
              
        #0 = Grande 3 = Petite
        #initialisation des pièces sur la tour 0
        self.tabPiecePosition = [0,0,0,0]
        

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
        if start==3:
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
        if (self.canvas.coords(self.piece[i])[1] >= 150):
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
        if(self.canvas.coords(self.piece[i])[0] <= POSITION[pos] - PIECE_W[i] + PILLIER_W ):
            self.canvas.move(self.piece[i], STEP, 0)  
        else:
            self.cmptMovDessin +=1
    def movementLeft(self,i, pos):
        #deplacement vers la gauche jusqu'au coordonées de la tour visée
        if(self.canvas.coords(self.piece[i])[0] >= POSITION[pos] - PIECE_W[i] +PILLIER_W ):
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