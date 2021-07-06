"""
---------------------------------------------------------------
#Projet NSI Novembre 2020
---------------------------------------------------------------
Je vous propose d'enrichir le script ci-dessous avec les éléments suivants :

- Une personnalisation de l'interface graphique en modifiant l'apparence et les couleurs utilisées.
- Changer l'icône de l'application.
- L'insertion de nouveaux boutons pour :
    a) retourner l'image verticalement (voir les scripts du TP04 mais on peut aussi utiliser la fonction rotate() en Python).
    b) retourner l'image horizontalement.
    c) permettre la transformation de l'image en niveau de gris (en utilisant les boucles for).
    d) permettre la transformation de l'image en négatif (ou convertir un négatif vers des couleurs naturelles)
    e) modifier le contraste de l'image (découvrir par vous même  l'opération à utiliser sur le codage des pixels)
    f) sauvegarder l'image modifiée.
- Réunir toutes vos commandes sur un menu déroulant.
- Eviter que l'image puisse être déformée lors de l'affichage sur l'interface.


"""


from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image,ImageTk,ImageOps

thumbnail_width=150
windows_name_and_toolbar_height=40
display_start_x=thumbnail_width+15
apercu_position=[display_start_x,10]

def max_but_its_resolution(width,height):
    max_size=max(width,height)
    if max_size==width and max_size==height:
        state="="
        return state
    elif max_size==width:
        state="width"
        return state
    elif max_size==height:
        state="height"
        return state

def get_height_by_width_and_ratio(width,ratio):
    coeff=width/ratio[0]
    height=int(round(ratio[1]*coeff))
    return height

def get_width_by_height_and_ratio(height,ratio):
    coeff=height/ratio[1]
    width=int(round(ratio[0]*coeff))
    return width

def ouvrir():
    global img_ini # déclare une variable globale (elle sera utilisable dans toutes les fonctions)
    global img_ini_width
    global img_ini_height
    mon_canevas.delete(ALL) # on efface la fenêtre graphique puis on ouvre un menu fichier
    nom_de_fichier = tkinter.filedialog.askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('all files','.*')])
    
    img_ini = Image.open(nom_de_fichier) #charge l'image initiale
    img_ini_width,img_ini_height=img_ini.size
    if img_ini_width >= 1000 or img_ini_height >=1000:
        tkinter.messagebox.showwarning("Attention","La résolution de l'image est très élevé, chaque opération effectué prendra beaucoup de temps")

    #thumbnail
    global thumbnail_height
    global thumbnail
    thumbnail=img_ini.copy() #Copie l'image initiale
    thumbnail_height=get_height_by_width_and_ratio(thumbnail_width,img_ini.size) #calcule la hauteur de la miniature a partir de sa largeur et de la taille originale
    thumbnail= thumbnail.resize((thumbnail_width,thumbnail_height), Image.ANTIALIAS)   #redimensionne l'image pour l'affichage
    thumbnail_object = ImageTk.PhotoImage(thumbnail) #Déclare l'objet thumbnail_object qui est une image
    mon_canevas.create_image(10, 10, anchor=NW, image=thumbnail_object) #Affiche l'objet thumbnail_object
    
    #apercu
    global apercu_width
    global apercu_height
    apercu=img_ini.copy() #Copie l'image initiale
    if max_but_its_resolution(img_ini_width,img_ini_height)=="width": #si img_ini est plus large que haute
        apercu_width=screen_width-thumbnail_width #largeur de tout l'écran moins la largeur de la miniature pour ne pas se chevaucher
        apercu_height=get_height_by_width_and_ratio(apercu_width,img_ini.size) #hauteur en fonction de la largeur et de la taille de img_ini
        if apercu_height > screen_height: #si l'image dépasse toujours en hauteur
            apercu_height=screen_height-windows_name_and_toolbar_height #screen height moins d'autres hauteur pour ne pas se chevaucher
            apercu_width=get_width_by_height_and_ratio(apercu_height,img_ini.size) #largeur en fonction de la hauteur et de la taille de img_ini
        apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS) #redimensionne l'image pour l'affichage
    else : #si img_ini est plus haute qu large ou si elle est carrée
        apercu_height=screen_height-windows_name_and_toolbar_height #screen height moins d'autres hauteur pour ne pas se chevaucher
        apercu_width=get_width_by_height_and_ratio(apercu_height,img_ini.size) #largeur en fonction de la hauteur et de la taille de img_ini
        apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS) #redimensionne l'image pour l'affichage
    apercu = ImageTk.PhotoImage(apercu) #Déclare l'objet apercu_object qui est une image
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu) #Affiche l'objet apercu_object

     #taille img_ini supérieure a apercu
    global img_ini_lower_res_apercu
    if img_ini_width < apercu_width:
        img_ini_lower_res_apercu=True
    else:
        img_ini_lower_res_apercu=False
    
    mainloop()


def changer_luminosite(image,correction):
    size_x,size_y = image.size
    #parcourt tous les pixels de l'image
    for x in range(size_x):
        for y in range(size_y):
            #ajoute la valeur de correction d'intensité à toutes les composantes RVB
            R=image.getpixel((x,y))[0]+correction
            V=image.getpixel((x,y))[1]+correction
            B=image.getpixel((x,y))[2]+correction
            #gestion des dépassements
            if R>255: R=255
            if V>255: V=255
            if B>255: B=255
            if R<0: R=0
            if V<0: V=0
            if B<0: B=0
            image.putpixel((x,y),(int(R),int(V),int(B))) #corrige le pixel avec sa nouvelle valeur
    return image

def niveau_gris():
    global img_ini
    #parcourt tous les pixels de l'image
    for x in range(img_ini_width):
        for y in range(img_ini_height):
            #récupère les valeurs RVB et les corrige
            R=img_ini.getpixel((x,y))[0]
            V=img_ini.getpixel((x,y))[1]
            B=img_ini.getpixel((x,y))[2]
            gris=int(round((0.299*R)+(0.587*V)+(0.114*B))) #conversion niveaux de gris
            img_ini.putpixel((x,y),(gris,gris,gris)) #applique le niveau de gris au pixel
    #affiche l'apercu
    apercu=img_ini.copy()
    apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS)
    apercu = ImageTk.PhotoImage(apercu)
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu)
    mainloop()

def inverser_couleur():
    global img_ini
    #parcourt tous les pixels de l'image
    for x in range(img_ini_width):
        for y in range(img_ini_height):
            #récupère les valeurs RVB et les inverse
            R=255-img_ini.getpixel((x,y))[0]
            V=255-img_ini.getpixel((x,y))[1]
            B=255-img_ini.getpixel((x,y))[2]
            img_ini.putpixel((x,y),(int(R),int(V),int(B))) #applique les couleurs inversés
    #affiche l'apercu
    apercu=img_ini.copy()
    apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS)
    apercu = ImageTk.PhotoImage(apercu)
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu)
    mainloop()

def changer_contraste(image,correction):
    global img_ini
    size_x,size_y = image.size
    #parcourt tous les pixels de l'image
    for x in range(size_x):
        for y in range(size_y):
            #récupère les valeurs RVB et appplique le contraste
            R=image.getpixel((x,y))[0]*correction
            V=image.getpixel((x,y))[1]*correction
            B=image.getpixel((x,y))[2]*correction
            #gestion des dépassements
            if R>255: R=255
            if V>255: V=255
            if B>255: B=255
            if R<0: R=0
            if V<0: V=0
            if B<0: B=0
            image.putpixel((x,y),(int(R),int(V),int(B))) #applique les couleurs avec le nouveau contraste
    return image

def symetrie_x():
    global img_ini
    img_ini=ImageOps.mirror(img_ini)
    #affiche l'apercu
    apercu=img_ini.copy()
    apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS)
    apercu = ImageTk.PhotoImage(apercu)
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu)
    mainloop()

def symetrie_y():
    global img_ini
    img_ini=ImageOps.flip(img_ini)
    #affiche l'apercu
    apercu=img_ini.copy()
    apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS)
    apercu = ImageTk.PhotoImage(apercu)
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu)
    mainloop()

def save():
    global img_ini
    nom_de_fichier = tkinter.filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[('jpg files','.jpg'),('all files','.*')])
    img_ini=img_ini.save(nom_de_fichier)

def fermer():
    mon_canevas.delete(ALL)
    Root.title("Image")

def aide():
    tkinter.messagebox.showinfo("Aide","Quand même, ce logiciel est super simple a utiliser, faites un effort bon sang !!!")

def features():
    tkinter.messagebox.showinfo("Fonctionnalités","-Miniature pour voir l'image d'origine\n-Réglage automatique de la taille de l'aperçu\n-Processus optimisé pour une latence plus faible\n-Menu enregistrer/sauvegarder\n-Système d'aperçu pour régler avant d'appliquer les effets")

def popup_lum():
    global img_ini
    global thumbnail
    popup = Toplevel()
    popup.title("Luminosité")
    popup.config(bg='#262626')
    popup.iconbitmap('windows_photo.ico') #charge un incone
    #####affichage image#####
    global caneva_popup
    caneva_popup = Canvas(popup,width=thumbnail_width, height=thumbnail_height+10, background='#262626', highlightthickness=0 ) #crée un caneva et enleve le cadre
    caneva_popup.pack()
    thumbnail_object = img_ini.copy()
    thumbnail_object = thumbnail_object.resize((thumbnail_width,thumbnail_height), Image.ANTIALIAS)
    thumbnail_object = ImageTk.PhotoImage(thumbnail_object) #Déclare l'objet thumbnail_object qui est une image
    caneva_popup.create_image(0, 10, anchor=NW, image=thumbnail_object) #Affiche l'objet thumbnail_object
    #########################
    global curseur_lum
    curseur_lum=Scale(popup, orient='horizontal', from_=-255, to=255,resolution=5, tickinterval=100, length=200, background='#E5C503', troughcolor='#000000',label='Luminosité', highlightbackground ='#000000', highlightcolor='#000000')
    curseur_lum.pack(side=LEFT , padx=50, pady=10)
    btn_apercu_lum = Button(popup, text="Aperçu", command=apercu_luminosite)
    btn_apercu_lum.pack(side=LEFT , padx=10)
    btn_appliquer_lum = Button(popup, text="Appliquer", command=appliquer_luminosite)
    btn_appliquer_lum.pack(side=LEFT , padx=10)
    popup.transient(Root) 	  # Réduction popup impossible 
    popup.grab_set()		  # Interaction avec fenetre jeu impossible
    popup.wait_window(popup)   # Arrêt script principal
    
def apercu_luminosite():
    correction = float(curseur_lum.get()) #recupère la valeur vue sur le Scale
    apercu = img_ini.copy()
    apercu = apercu.resize((thumbnail_width,thumbnail_height), Image.ANTIALIAS)
    apercu = changer_luminosite(apercu, correction)
    apercu = ImageTk.PhotoImage(apercu)
    caneva_popup.create_image(0, 10, anchor=NW, image=apercu)
    mainloop()

def appliquer_luminosite():
    global img_ini
    correction = float(curseur_lum.get()) #recupère la valeur vue sur le Scale
    img_ini = changer_luminosite(img_ini, correction)
    #affiche l'apercu
    apercu=img_ini.copy()
    apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS)
    apercu = ImageTk.PhotoImage(apercu)
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu)
    mainloop()

def popup_con():
    global img_ini
    global thumbnail
    popup = Toplevel()
    popup.title("Contraste")
    popup.config(bg='#262626')
    popup.iconbitmap('windows_photo.ico') #charge un incone
    #####affichage image#####
    global caneva_popup
    caneva_popup = Canvas(popup,width=thumbnail_width, height=thumbnail_height+10, background='#262626', highlightthickness=0 ) #crée un caneva et enleve le cadre
    caneva_popup.pack()
    thumbnail_object = img_ini.copy()
    thumbnail_object = thumbnail_object.resize((thumbnail_width,thumbnail_height), Image.ANTIALIAS)
    thumbnail_object = ImageTk.PhotoImage(thumbnail_object) #Déclare l'objet thumbnail_object qui est une image
    caneva_popup.create_image(0, 10, anchor=NW, image=thumbnail_object) #Affiche l'objet thumbnail_object
    #########################
    global curseur_con
    curseur_con=Scale(popup, orient='horizontal', from_=1, to=255,resolution=1, tickinterval=100, length=200, background='#E5C503', troughcolor='#000000',label='Contraste', highlightbackground ='#000000', highlightcolor='#000000')
    curseur_con.pack(side=LEFT , padx=50, pady=10)
    btn_apercu_lum = Button(popup, text="Aperçu", command=apercu_contraste)
    btn_apercu_lum.pack(side=LEFT , padx=10)
    btn_appliquer_lum = Button(popup, text="Appliquer", command=appliquer_contraste)
    btn_appliquer_lum.pack(side=LEFT , padx=10)
    popup.transient(Root) 	  # Réduction popup impossible 
    popup.grab_set()		  # Interaction avec fenetre jeu impossible
    popup.wait_window(popup)   # Arrêt script principal

def apercu_contraste():
    correction = float(curseur_con.get()) #recupère la valeur vue sur le Scale
    apercu = img_ini.copy()
    apercu = apercu.resize((thumbnail_width,thumbnail_height), Image.ANTIALIAS)
    apercu = changer_contraste(apercu, correction)
    apercu = ImageTk.PhotoImage(apercu)
    caneva_popup.create_image(0, 10, anchor=NW, image=apercu)
    mainloop()

def appliquer_contraste():
    global img_ini
    correction = float(curseur_con.get()) #recupère la valeur vue sur le Scale
    img_ini = changer_contraste(img_ini, correction)
    #affiche l'apercu
    apercu=img_ini.copy()
    apercu=apercu.resize((apercu_width,apercu_height), Image.ANTIALIAS)
    apercu = ImageTk.PhotoImage(apercu)
    mon_canevas.create_image(apercu_position, anchor=NW, image=apercu)
    mainloop()

#création d'une fenêtre graphique
Root = Tk()
Root.title("Théo PERNEL retouche basique d'images") #nom de la fenêtre
Root.iconbitmap('windows_photo.ico') #charge un incone
screen_width=Root.winfo_screenwidth() #récupère la résolution x de l'écran
screen_height=Root.winfo_screenheight() #récupère la résolution y de l'écran
Root.geometry("%dx%d+0+0" % (screen_width,screen_height)) #dimensionne la fenêtre aux dimensions de l'écran
Root.state("zoomed") #démarre en fenêtre agrandie

#création d'un menu associé à la fenêtre
mon_menu = Menu(Root)

menuFichier = Menu(mon_menu,tearoff=0)
menuFichier.add_command(label="Ouvrir une image",command=ouvrir)
menuFichier.add_command(label="Fermer l'image",command=fermer)
menuFichier.add_command(label="Enregistrer",command=save, background='#3492EB')
menuFichier.add_command(label="Quitter", command=Root.destroy, background='#660000')
mon_menu.add_cascade(label="Fichier", menu=menuFichier)

menuEdition=Menu(mon_menu,tearoff=0)
menuEdition.add_command(label="Symétrie X",command=symetrie_x)
menuEdition.add_command(label="Symétrie Y",command=symetrie_y)
menuEdition.add_command(label="Niveau de gris",command=niveau_gris)
menuEdition.add_command(label="Inverser couleur",command=inverser_couleur)
menuEdition.add_command(label="Luminosité",command=popup_lum)
menuEdition.add_command(label="Contraste",command=popup_con)
mon_menu.add_cascade(label="Édition", menu=menuEdition)

menuPlus = Menu(mon_menu,tearoff=0)
menuPlus.add_command(label="Aide",command=aide)
menuPlus.add_command(label="Fonctionnalités",command=features)
mon_menu.add_cascade(label="Plus", menu=menuPlus)

# Affichage du menu
Root.config(menu=mon_menu)
Root.config(bg='#262626')

# Création d'un widget Canvas (toile)
canvas_height=screen_height-windows_name_and_toolbar_height
canvas_width=screen_width

mon_canevas = Canvas(Root,width=canvas_width, height=canvas_height, background='#737373', highlightbackground='#E5C503', highlightcolor='#E5C503')
mon_canevas.pack(padx=10,pady=10)

Root.mainloop()

#highlightthickness=10 //modifie la largeur de la bordure