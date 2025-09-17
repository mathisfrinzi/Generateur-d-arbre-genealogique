# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 19:11:51 2024

@author: mathf
"""

import requests
import csv
from io import StringIO
from tkinter import *
import math
import random
from IPython.display import display
from PIL import Image, ImageDraw, ImageFont

def fetch_sheet_as_csv(sheet_url):
    # Télécharger le contenu CSV à partir de l'URL fournie
    response = requests.get(sheet_url)
    response.raise_for_status()  # Vérifiez que la requête a réussi

    # Lire le contenu CSV
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(StringIO(csv_content))

    # Convertir les données CSV en une liste de listes
    data = list(csv_reader)
    return data

# URL de la feuille Google Sheets publiée en tant que CSV
sheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQmeX1xZ8R50EPiGRLrXYoqdC2KBYGmxpzXRPvt3hp2za9nn02EvUEECU7aW4xeSmz1n6Yp6w0LbXKI/pub?gid=0&single=true&output=csv'
sheet_url = 'https://docs.google.com/spreadsheets/d/1I_Yv4g2akyRJRcndJdzrrYfHrjwiCYxrtptrOJ95YhU/export?format=csv&gid=79602097'
data_rel = fetch_sheet_as_csv(sheet_url)
CLEF_REL = {}
a = data_rel[0]
del data_rel[0]
for i in range(len(a)):
    CLEF_REL[a[i]] = i
print('\nRécupération des datas de la feuille Relation :')
print(data_rel)
urlbis = 'https://docs.google.com/spreadsheets/d/1I_Yv4g2akyRJRcndJdzrrYfHrjwiCYxrtptrOJ95YhU/export?format=csv&gid=0'
data_prof = fetch_sheet_as_csv(urlbis)
CLEF_PROF = {}
b = data_prof[0]
del data_prof[0]
for i in range(len(b)):
    CLEF_PROF[b[i]] = i
print('\nRécupération des datas de la feuille Profil :')
print(data_prof)





class Arbre():
    ListeArbre = {}
    def __init__(self, etage):
        self.etage = etage
        Arbre.ListeArbre[self.etage] = self
        self.liste_intro = []
    
class Intronisable:
    ListeIntronisable = {}
    def __init__(self, _id, etage, surnom, promo, chambre, photo, ordre=0):
        self.etage = etage
        self.surnom = surnom
        self.id = _id
        Intronisable.ListeIntronisable[self.id] = self
        self.promo = promo
        self.photo = photo
        self.chambre = chambre
        if ordre == '':
            ordre = 0
        self.ordre = ordre
        self.liste_parrains = []
        self.liste_fillots = [] #liste des ids des fillots
    def first_parrain(self,etage):
        for i in self.liste_parrains:
            if get_personne(i).etage == etage:
                return i
    def __str__(self):
        return '{0} {1}E{2} {3}, {4}'.format(self.etage, self.surnom, self.promo, self.chambre, self.liste_fillots)
        
def get_id(etage, surnom, promo):
    for i in Intronisable.ListeIntronisable.keys():
        profil = Intronisable.ListeIntronisable[i]
        if profil.surnom == surnom and profil.etage == etage and profil.promo == promo:
            return i

def get_id_sans_promo(etage,surnom):
    for i in Intronisable.ListeIntronisable.keys():
        profil = Intronisable.ListeIntronisable[i]
        if profil.surnom == surnom and profil.etage == etage:
            return i
    
def get_personne(_id):
    return Intronisable.ListeIntronisable[_id]
    
class Intronisation():
    ListeIntroFillotParrain = {}
    def __init__(self, etage, fillot_id, parrain_id):
        if fillot_id == parrain_id:
            return None
        self.etage = etage
        self.fillot = fillot_id
        self.parrain = parrain_id
        Intronisation.ListeIntroFillotParrain[(fillot_id,parrain_id)] = self
        Arbre.ListeArbre[etage].liste_intro.append(self)
        Intronisable.ListeIntronisable[parrain_id].liste_fillots.append(fillot_id)
        Intronisable.ListeIntronisable[fillot_id].liste_parrains.append(parrain_id)
       
def chercher_toutes_les_promos_sup(intronisable,promoinit,etage,liste=[],b=True):
    promo = intronisable.promo
    if promo > promoinit:
        liste.append((intronisable.promo,intronisable,b))
    if len(intronisable.liste_fillots) == 0:
        return liste
    for fillot in intronisable.liste_fillots:
        if Intronisation.ListeIntroFillotParrain[(fillot,intronisable.id)].etage == etage:
            fillot_ = get_personne(fillot)
            liste = chercher_toutes_les_promos_sup(fillot_,promoinit,etage,liste,b and promoinit!=fillot_.promo)
    return liste
  

def lst_sup(intronisable,etage):
    liste = chercher_toutes_les_promos_sup(intronisable, intronisable.promo, etage, [])
    return liste     

def esp(intronisable,etage,listing = False):
    l = lst_sup(intronisable,etage)
    if l == []:
        if listing:
            return []
        return 1
    m = min(l,key=lambda x:int(x[0]))[0]
    kri = []
    datekri = []
    esp_cpt = 0
    for f in l:
        (date,fillot,b) = f
        if (date == m and b) or (date in datekri and b) or ((fillot.id, intronisable.id) in Intronisation.ListeIntroFillotParrain.keys() and Intronisation.ListeIntroFillotParrain[(fillot.id, intronisable.id)].etage == etage) :
            continuee = True
            if date in datekri and b:
                parrain = get_personne(fillot.first_parrain(etage))
                stoptoutnow = False
                if parrain.promo == fillot.promo :
                    stoptoutnow = True
                while parrain.id != intronisable.id:
                    if stoptoutnow:
                        break
                    parrain_before = parrain
                    p_id = parrain.first_parrain(etage)
                    if p_id != None:
                        parrain = get_personne(p_id)
                        if parrain.promo == parrain_before.promo:
                            continuee = True
                            break
                        if parrain.id == intronisable.id:
                            continuee = False
                
                #parrain = get_personne(fillot.first_parrain(etage))
                #if parrain.id != intronisable.id:

                    #if parrain in kri and parrain.promo < fillot.promo:
                        #continuee = False
            if continuee:
                kri.append(fillot)
                datekri.append(fillot.promo)
                fillot__ = fillot
                
                while fillot__.first_parrain(etage) != intronisable.id:
                    if fillot__.first_parrain(etage) == None:
                        break
                    nfillot__ = get_personne(fillot__.first_parrain(etage))
                    if nfillot__.first_parrain(etage) == None:
                        break
                    fillot__ = nfillot__
                if fillot__.first_parrain(etage) == intronisable.id:
                    esp_cpt += esp(fillot, etage, False)
    if listing:
        return kri
    if esp_cpt == 0:
        return 1
    return esp_cpt
    
NFACTEUR = 12
class ArbreGraphique():
    HauteurCase = 12*NFACTEUR
    LongueurCase = 10*NFACTEUR
    DistanceCaseHaut = 4*NFACTEUR
    DistanceCaseLarge = 3*NFACTEUR
    DistanceTexteBordInf = 10
    PAD_TEXTE = 5
    def __init__(self, liste_coords_cases = [], liste_coords_noeud = [], listetexte = [], launch = True):
        self.fenetre = Tk()
        self.liste_coords_cases = liste_coords_cases
        self.liste_coords_noeud = liste_coords_noeud
        self.listetexte = listetexte
        self.canvas = Canvas(self.fenetre, width = 3000, height = 500)
        self.canvas.pack()
        self.poubelle = []
        self.origine = (-000,20)
        self.bouton = Button(self.fenetre, text = 'Display', command = self.display)
        self.bouton.pack()
        if launch:
            self.display()
        self.fenetre.mainloop()
    def display(self):
        for i in self.poubelle:
            self.canvas.delete(self.fenetre, i)
        for i in self.liste_coords_noeud:
            self.poubelle.append(self.canvas.create_line(self.origine[0]+i[0],self.origine[1]+i[1],self.origine[0]+i[2],self.origine[1]+i[3]))
        for i in self.liste_coords_cases:
            self.poubelle.append(self.canvas.create_rectangle(self.origine[0]+i[0]-ArbreGraphique.LongueurCase//2, i[1]-ArbreGraphique.HauteurCase//2+self.origine[1], self.origine[0]+i[0]+ArbreGraphique.LongueurCase//2, self.origine[1]+i[1]+ArbreGraphique.HauteurCase//2, fill='white'))
        for i in self.listetexte:
            self.poubelle.append(self.canvas.create_text(self.origine[0]+i[0],self.origine[1]+i[1],text = i[2]))
    def ajoute_case(self,x,y):
        self.liste_coords_cases.append((x,y))

liste_etage = []
for i in range(len(data_rel)):
    if not data_rel[i][CLEF_REL['Etage']] in liste_etage:
        v = data_rel[i][CLEF_REL['Etage']]
        if v != '':
            liste_etage.append(v)
        


for etage in liste_etage:
    Arbre(etage)

for k in data_prof:
    Intronisable(k[CLEF_PROF['ID']],k[CLEF_PROF['Etage']], k[CLEF_PROF['Surnom']],k[CLEF_PROF['Promo']], k[CLEF_PROF['Chambre']], k[CLEF_PROF['Photo']], k[CLEF_PROF['Ordre source']])

for k in data_rel:
    Intronisation(k[CLEF_REL['Etage']], k[CLEF_REL['ID Fillot']], k[CLEF_REL['ID Parrain']])

SAVE = {}
ALREADY_GEN = []
ARELIER = []
ARELIERBIS = []
NOMBRE_CASE = 0
Source_initial_save = {}

def est_fillot(fillot,parrain,etage):
    return (fillot,parrain) in Intronisation.ListeIntroFillotParrain.keys() and Intronisation.ListeIntroFillotParrain[(fillot,parrain)].etage == etage

def generate_case_source(source,etage, origine = (0,0),liste = [], liste_noeud = [], promo_source = None, listetexte = [], source_avant = None, source_init = None):
    global NOMBRE_CASE, ARELIER
    if source not in ALREADY_GEN:
        #print('Génération de la case {0} de :'.format(NOMBRE_CASE), get_personne(source).surnom)
        
        ALREADY_GEN.append(source)
        personne = get_personne(source)
        if promo_source == None:
            promo_source = personne.promo
        if source_init == None:
            source_init = source
        SAVE[source] = origine
        NOMBRE_CASE += 1
        
        #print('Case en ',origine)
        if personne.photo.upper() != "FICTIF":
            liste.append(origine)   
            listetexte.append((origine[0],origine[1]+ArbreGraphique.HauteurCase//2-ArbreGraphique.DistanceTexteBordInf, personne.surnom, personne))#+' '+str(esp(get_personne(source),etage))))
        
        Source_initial_save[source] = source_init
        
        n = esp(get_personne(source),etage)
        kri = esp(get_personne(source),etage,True)
        taille = ArbreGraphique.LongueurCase*n + ArbreGraphique.DistanceCaseLarge*(n-1)
        creneau = taille//n
        cpt = 0
        maxiori = -math.inf
        miniori = math.inf
        
        possede_fillot = False
        for fillot in get_personne(source).liste_fillots:
            if est_fillot(fillot,source,etage):
                possede_fillot = True
                break
        
        for i in kri:
            RELATIONFILLOT = est_fillot(i.id,source,etage)
            p = esp(i, etage)
            ori = (origine[0]-taille//2+p*creneau//2+cpt,origine[1]-(ArbreGraphique.HauteurCase+ArbreGraphique.DistanceCaseHaut)*(int(promo_source)-int(i.promo)))
            if RELATIONFILLOT and i.id not in ALREADY_GEN and personne.photo.upper() != 'FICTIF':
                liste_noeud.append((ori[0],ori[1],ori[0],origine[1]+(ArbreGraphique.DistanceCaseHaut+ArbreGraphique.HauteurCase)//2))
            else:
                for parrain in i.liste_parrains:
                    if i.promo == get_personne(parrain).promo and Intronisation.ListeIntroFillotParrain[(i.id,parrain)].etage == etage:
                        ARELIER.append((i.id,parrain))
            generate_case_source(i.id, etage, ori, liste=liste, liste_noeud=liste_noeud, listetexte=listetexte,source_avant=source, source_init = source_init)
            cpt += p*creneau
            if RELATIONFILLOT:
                fillot__ = i
                while fillot__.first_parrain(etage) != source:
                    if fillot__.first_parrain(etage) == None:
                        break
                    fillot__ = get_personne(fillot__.first_parrain(etage))
                if fillot__.first_parrain(etage) == source:
                    if ori[0] < miniori:
                        miniori = ori[0]
                    if ori[0] > maxiori:
                        maxiori = ori[0]
        y = origine[1]+(ArbreGraphique.DistanceCaseHaut+ArbreGraphique.HauteurCase)//2
        miniori = min(miniori, origine[0])
        maxiori = max(maxiori, origine[0])
        if possede_fillot :
            if personne.photo.upper() != 'FICTIF':
                liste_noeud.append((miniori,y, maxiori,y))
                liste_noeud.append((origine[0],origine[1],origine[0],y))
    else:
        ARELIERBIS.append((source,source_avant))
    return [liste,liste_noeud,listetexte,ARELIER]
    
def generate_final(source,etage, texte = True, origine = (0,0)):
    l,ln,lt,a = generate_case_source(source,etage, origine = origine, liste = [],liste_noeud=[],listetexte=[])
    if not texte:
        lt = []
    return l,ln,lt


def obtenir_sources(etage):
    src = []
    liste_id = []
    for i in data_prof:
        liste_id.append(i[CLEF_PROF['ID']])
    
    while len(liste_id) != 0:
        a = liste_id.pop()
        in_ = False
        for i in Intronisation.ListeIntroFillotParrain.keys():
            if i[0] == a and Intronisation.ListeIntroFillotParrain[i].etage == etage:
                in_ = True
                break
        if not in_:
            src.append(a)
    
    src_copy = []
    for i in src:
        in_ = False
        if get_personne(i).etage == etage:
            in_= True
            
        for j in Intronisation.ListeIntroFillotParrain.keys():
            if j[1] == i and Intronisation.ListeIntroFillotParrain[j].etage == etage:
                in_ = True
                break
        if in_:
            src_copy.append(i)
    src = src_copy
    return src
         
def trier_sources(value):
    if get_personne(value).ordre == '':
        return 0
    return int(get_personne(value).ordre)

def generate_sources(etage, origine = (0,0)):
    LAST_SOURCE = []
    src = obtenir_sources(etage)
    src.sort(key=trier_sources)
    #tri source
    
    def rec(etage,origine,src):
        print("\nGénération d'un arbre à partir de la source :")
        print(src)
        print([get_personne(i).surnom for i in src])
        LAST_SOURCE.append(src)
        global ARELIERBIS, ALREADY_GEN, NOMBRE_CASE, ARELIER, SAVE
        ARELIERBIS = []
        ARELIER = []
        ALREADY_GEN = []
        SAVE = {}
        cpt = origine[0]
        NOMBRE_CASE=0
        L = []
        LN = []
        LT = []
        for i in src:
            k = esp(get_personne(i),etage)
            
            y__ = origine[1]+(ArbreGraphique.HauteurCase+ArbreGraphique.DistanceCaseHaut)*(int(get_personne(i).promo)-int(mindate))
            l,ln,lt = generate_final(i,etage, origine = (cpt+(ArbreGraphique.LongueurCase*k + ArbreGraphique.DistanceCaseLarge*(k-1))//2,y__))
            cpt += (ArbreGraphique.LongueurCase*k + ArbreGraphique.DistanceCaseLarge*(k-1))
            L+=l
            LN+=ln
            LT+=lt            
            cpt += ArbreGraphique.DistanceCaseLarge
        
        for i in ARELIERBIS:
            a,b=(Source_initial_save[i[0]], Source_initial_save[i[1]])
            c,d = src.index(a),src.index(b)
            if c!=d and c!=(d-1) and c!=(d+1):
                print('\nModification de la source')
                print(src)
                src.remove(b)
                try:
                    print('coucou', get_personne(src[c]).surnom, get_personne(src[d]).surnom)
                    booleean = get_personne(src[c]).ordre < get_personne(src[d]).ordre
                    print('ok', booleean)
                except:
                    booleean = bool(random.choice([0,1]))
                
                if booleean:
                    try:
                        src.insert(c+1,b)
                    except:
                        src.insert(c,b)
                else:
                    try:
                        src.insert(c,b)
                    except:
                        src.insert(c+1,b)
                print(src)
                if LAST_SOURCE.count(src) <= 20:
                    L=[]
                    LN=[]
                    LT=[]
                    return rec(etage,origine,src)
            if (i[0],i[1]) in Intronisation.ListeIntroFillotParrain.keys() and Intronisation.ListeIntroFillotParrain[(i[0],i[1])].etage == etage:
                #print('Correction Double parrain : {0} {1}'.format(get_personne(i[0]).surnom,get_personne(i[1]).surnom))
                origine_fillot = SAVE[i[0]]
                origine_parrain = SAVE[i[1]]
                y_ = origine_fillot[1]-ArbreGraphique.HauteurCase//2-2*ArbreGraphique.DistanceCaseHaut//3
                LN.append((origine_fillot[0],origine_fillot[1],origine_fillot[0],y_))
                x_ = origine_parrain[0]-ArbreGraphique.LongueurCase//2-2*ArbreGraphique.DistanceCaseLarge//3
                LN.append((origine_fillot[0],y_,x_,y_))
                y__ = origine_parrain[1]+ArbreGraphique.HauteurCase//2+2*ArbreGraphique.DistanceCaseHaut//3
                LN.append((x_,y_,x_,y__))
                LN.append((x_,y__, origine_parrain[0],y__))
                LN.append((origine_parrain[0],y__,origine_parrain[0],origine_parrain[1]))
        for i in ARELIER:
            #print('Correction Fillot Même promo que parrain : ',get_personne(i[0]).surnom,'-',get_personne(i[1]).surnom)
            a = get_personne(i[0])
            b = get_personne(i[1])
            origine_fillot = SAVE[a.id]
            origine_parrain = SAVE[b.id]
            y_ = origine_fillot[1]-ArbreGraphique.HauteurCase//2-ArbreGraphique.DistanceCaseHaut//3
            y__ = origine_fillot[1]+ArbreGraphique.HauteurCase//2+ArbreGraphique.DistanceCaseHaut//2
            x_ = origine_fillot[0]-ArbreGraphique.LongueurCase//2-ArbreGraphique.DistanceCaseLarge//3
            LN.append((origine_fillot[0],origine_fillot[1],origine_fillot[0], y_))
            LN.append((origine_fillot[0],y_,x_,y_))
            LN.append((x_,y__,x_,y_))
            LN.append((x_,y__, origine_parrain[0],y__))
            
                
        return L,LN,LT
    return rec(etage,origine,src)

ASK = input("\nQuel étage veux tu générer ? écrire 'tous' pour tous les générer, écrire 'X2,T3' pour générer le X2 et le T3  : ")

if ASK.upper() == 'TOUS':
    ASK = liste_etage
else:
    ASK = ASK.split(',')


print("\nRécupération du fond et traitement de l'image")
image_fond = Image.open('Images/estiah_fond.jpg')

image_fond_retourne = image_fond.copy()
px_init = image_fond.load()
px_retourne = image_fond_retourne.load()
image_fond_inverse = image_fond.copy()
px_inverse = image_fond_inverse.load()
image_fond_inverse_retourne = image_fond.copy()
px_retourne_inverse = image_fond_inverse_retourne.load()
w,h = image_fond.size
for i in range(w):
    for j in range(h):
        px_retourne[i,j] = px_init[w-i-1,j]
        px_inverse[i,j] = px_init[i,h-1-j]
        px_retourne_inverse[i,j] = px_init[w-i-1,h-1-j]
        
        
logo_design = Image.open('Images/logo_design.png')

TAILLE_LOGO = 300
TAILLE_DATE = 200
logo_design = logo_design.resize((TAILLE_LOGO-20,TAILLE_LOGO-20))


print('\nGénération de {0}'.format(ASK))

for ETAGE_ in ASK:
    print("\nDémarrage de la génération de l'arbre {0}".format(ETAGE_))
    
    mindate = 2026
    maxdate = 0
    for i in data_prof:
        if i[CLEF_PROF['Etage']] != ETAGE_ or i[CLEF_PROF['Photo']].upper() == 'FICTIF':
            continue
        dd = int(i[CLEF_PROF['Promo']])
        if dd<mindate:
            mindate = dd
        if dd>maxdate:
            maxdate = dd
    n=0
    for i in obtenir_sources(ETAGE_):
        n += esp(get_personne(i),ETAGE_)
    G=generate_sources(ETAGE_, origine = (10+ArbreGraphique.LongueurCase,10+ArbreGraphique.HauteurCase))
    L,LN,LT = G
    if False:
        ArbreGraphique(*G)
    espace_logo = TAILLE_LOGO
    W=espace_logo+(ArbreGraphique.LongueurCase*n + ArbreGraphique.DistanceCaseLarge*(n-1))+20+2*ArbreGraphique.LongueurCase+TAILLE_DATE
    p = maxdate-mindate
    H = 10+(ArbreGraphique.HauteurCase*(p+1) + ArbreGraphique.DistanceCaseHaut*(p+1))+20+2*ArbreGraphique.HauteurCase
    ## L'arbre généalogique est généré, il faut maintenant le transmettre sur une image
    def create_image(w, h, path='lien.png', color=(255, 255, 255)):
        if w==0:
            w+=1
        if h==0:
            h+=1
        image = Image.new('RGB', (w, h), color=color)
        image.save(path)
        return image
    
    def save_image(image,path):
        image.save(path)
    
    def afficher(image):
        display(image)
        
    def getPixel(x: int, y: int, px) -> tuple:
        return px[x,y]
    
    def setPixel(x,y,px,color):
        if 0<x<W and 0<y<H:
            px[x,y] = color
        
    def create_line(x0,y0,x1,y1,px, color):
        
        x0,x1 = min(x0,x1),max(x0,x1)
        y0,y1 = min(y0,y1),max(y0,y1)
        if x0 == x1:
            for i in range(y0,y1):
                setPixel(x0,i,px,color)
        elif y0 == y1:
            for i in range(x0,x1):
                setPixel(i,y0,px,color)
        else:
            a = (y1-y0)/(x1-x0)
            for x in range(x0,x1):
                y = int(y0+a*(x-x0))
                setPixel(x,y,px,color)
                
    def create_rectangle(x0,y0,x1,y1,px,color):
        x0,x1 = min(x0,x1),max(x0,x1)
        y0,y1 = min(y0,y1),max(y0,y1)
        for i in range(x0,x1):
            for j in range(y0,y1):
                setPixel(i,j,px,color)
                
                
    def draw_text(image, text, position, font_size=24, color=(0, 0, 0),center=False, font='arial.ttf'):
        if center:
            return draw_centered_text(image,text,position,font_size,color)
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype(font, font_size)  # Assurez-vous que la police est disponible
        except IOError:
            print(font,'problem')
            font = ImageFont.load_default()  
        draw.text(position, text, fill=color, font=font)
        
    def draw_centered_text(image, text, position, font = 'arial.ttf', font_size=24, color=(0, 0, 0)):
        draw = ImageDraw.Draw(image)
        
        # Charger une police (ou utiliser une police par défaut si non disponible)
        try:
            font = ImageFont.truetype(font, font_size)  # Assurez-vous que la police est disponible
        except IOError:
            print(font,'problem')
            font = ImageFont.load_default(font_size)  # Police par défaut
    
        # Obtenir la taille du texte
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]  # largeur du texte
        text_height = text_bbox[3] - text_bbox[1]  # hauteur du texte
    
        # Calculer la position du coin supérieur gauche pour centrer le texte
        x = position[0] - text_width // 2
        y = position[1] - text_height // 2
    
        # Dessiner le texte
        draw.text((x, y), text, fill=color, font=font)
             
    def poser_image(image, xsupgauche, ysupgauche, imbase):
        imbase.paste(image, (xsupgauche, ysupgauche))
   
    image = create_image(W,H,path='{0}.pdf'.format(ETAGE_))
    px = image.load()
    #Mise en place du fond
    cpt = 0 
    NCPTMOD2 = 0
    while cpt<W:
        if NCPTMOD2%2 == 0:
            poser_image(image_fond,cpt,0,image)
            poser_image(image_fond_inverse, cpt, image_fond.size[1],image)
        if NCPTMOD2%2 == 1:
            poser_image(image_fond_retourne,cpt,0,image)
            poser_image(image_fond_inverse_retourne, cpt, image_fond.size[1],image)
        cpt+=image_fond.size[0]
        NCPTMOD2 += 1
        
    create_rectangle(W,H,W-TAILLE_LOGO,0,px,(255,255,255))
    poser_image(logo_design,W-TAILLE_LOGO+10,H-TAILLE_LOGO+10,image)

    for tup in LN:
        x0,y0,x1,y1 = tup
        create_line(x0,y0,x1,y1,px,(255,255,255))
        create_line(x0+1,y0,x1+1,y1,px,(255,255,255))
        create_line(x0,y0+1,x1,y1+1,px,(255,255,255))
    lien = 'Images/default{0}.png'
    imdefaut = Image.open(lien.format(ETAGE_))
    for i in range(len(L)):
        tup = L[i]
        surnom = LT[i][2]
        personne_ = LT[i][3]
        if personne_.photo.upper() == 'FICTIF':
            continue
        x,y = tup
        
        try:
            try:
                lien='Images/{0}-{1}.png'.format(personne_.id,surnom)
                imcase = Image.open(lien)
            except:
                try:
                    lien='Images/{0}-{1}.jpg'.format(personne_.id,surnom)
                    imcase = Image.open(lien)
                except:
                    lien ='Images/{0}-{1}.jpeg'.format(personne_.id,surnom)
                    imcase = Image.open(lien)
        except :
            try:
                try:
                    lien='Images/{0}.png'.format(personne_.id)
                    imcase = Image.open(lien)
                except :
                    try:
                        lien='Images/{0}.jpg'.format(personne_.id)
                        imcase = Image.open(lien)
                    except :
                        lien ='Images/{0}.jpeg'.format(personne_.id)
                        imcase = Image.open(lien)
            except:
                imcase = imdefaut
        p = ArbreGraphique.PAD_TEXTE
        h_im = ArbreGraphique.HauteurCase-2*p-2*ArbreGraphique.DistanceTexteBordInf
        w_im =int((1/1.2)*h_im)
        imcase = imcase.resize((w_im,h_im))
        
        x0 = x-ArbreGraphique.LongueurCase//2
        x1 = x+ArbreGraphique.LongueurCase//2
        y0 = y-ArbreGraphique.HauteurCase//2
        y1 = y+ArbreGraphique.HauteurCase//2
        create_rectangle(x0,y0,x1,y1,px,(255,255,255))
        poser_image(imcase,x-imcase.size[0]//2,y0+ArbreGraphique.PAD_TEXTE, image)
        #print("Génération de l'image de : {0}".format(get_personne(get_id_sans_promo(etage,surnom)).surnom))
        
    for tup in LT:
        x,y,texte,personne = tup
        if personne.photo.upper() == 'FICTIF':
            continue
        if personne.chambre.upper() not in ['Affilié'.upper(),'Affiliée'.upper(),'','Exté'.upper(),'?'.upper()]:
            texte += ' - '+str(personne.chambre)
        draw_centered_text(image,texte,(x,y),color=(0,0,0),font_size=12, font='bahnschrift.ttf')
    
    cpty = ArbreGraphique.HauteurCase
    XDATE = W-espace_logo-TAILLE_DATE//2
    for date in range(mindate,maxdate+1):
        delta = ArbreGraphique.DistanceCaseHaut+ArbreGraphique.HauteurCase
        
        draw_centered_text(image,str(date),(XDATE-50,cpty),color=(255,255,255), font_size = min(TAILLE_DATE//2,delta), font = 'impact.ttf')
        cpty += delta
    
    draw_centered_text(image,ETAGE_,(W-TAILLE_LOGO//2,TAILLE_LOGO//2),font='tahomabd.ttf',color = (0,0,0),font_size = TAILLE_LOGO//2)
    
    save_image(image,'{0}.pdf'.format(ETAGE_))
    print('Génération du fichier {0}.pdf'.format(ETAGE_))
    

    
    
