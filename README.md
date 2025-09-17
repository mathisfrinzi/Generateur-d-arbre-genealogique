# Générateur d'arbre généalogique
Programme qui génère automatiquement un arbre représentant les relations de parrainage de Centrale Lyon.

## Requis : 
Les polices d'écriture : arial.ttf, bahnschrift.ttf, tahomabd.ttf.

## Notice d'installation :
1 - Télécharger le fichier arbre-genealogique.py et le fichier Images.

2 - Lancer le fichier arbre-genealogique.py et choisir les arbres à générer.

3 - Les arbres générés au format PDF sont présents dans le dossier principal (pour des raisons d'anonymat, les photos ne sont pas générées).

# Comment se réapproprier le programme :
## 1 - Adapter les données
Créer un fichier Google Sheets dont le format des données est similaire.

## 2 - Adapter les graphismes.
Dans le fichier arbre-genealogique.py, il faut supprimer certaines parties si on ne veut pas les voir apparaître sur l'arbre : 

- Suppression des dates (pas adaptées à un arbre généalogique plus classique) :
Supprimer la ligne de code :

    for date in range(mindate,maxdate+1):
        delta = ArbreGraphique.DistanceCaseHaut+ArbreGraphique.HauteurCase        
        draw_centered_text(image,str(date),(XDATE-50,cpty),color=(255,255,255), font_size = min(TAILLE_DATE//2,delta), font = 'impact.ttf')
        cpty += delta

-Supprimer le texte avec le nom de l'étage 
Supprimer la ligne de code :     
    draw_centered_text(image,ETAGE_,(W-TAILLE_LOGO//2,TAILLE_LOGO//2),font='tahomabd.ttf',color = (0,0,0),font_size = TAILLE_LOGO//2)

## 3 - Adapter les images :
Ajouter les images au format 4:5 dans le dossier images, pour les associer à un profil, il suffit de les renommer correctement. Par exemple pour l'ID 0, "0.png" devrait suffire. Le format des images doit être lisible par Python.

        
