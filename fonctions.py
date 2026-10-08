#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 14:43:01 2022
@author: VOS NOMS ET CLASSE ICI
BY-NC 4.0   (vous pouvez changer la licence, pour choisir une licence libre : https://creativecommons.org/choose/?lang=fr)
"""

############################################
#          IMPORTATION DES MODULES         #
# Vous pouvez bien sur en utiliser d'autre #
############################################

from PIL import Image as I
from IPython.display import Image, display, clear_output
import sys
import shutil

#############################################################################################
#                                       LES FONCTIONS                                       #
# Vous pouvez bien sur en ajouter ou en supprimer à votre guise                             #
# Pour l'instant ces fonctions ne retournent pas le bon résultat                            #
# mais elles permettent à l'élève en charge du programme prncipal de commencer à travailler.#
#############################################################################################

def selection_images():
    """
    selection des fichiers images source

    Returns
    -------
    img1 : image 1

    img2 : image 2
    
    new : image blanche
    les trois images ont les mêmes dimensions
    """
    
    img1 = str(input("Choisissez votre première image (avec l'extenssion) : "))
    img2 = str(input("Choisissez votre deuxième image (avec l'extenssion) : "))

    if img1 == "" or img2 == "":
        print("Un erreur est surveunue, veuillez recomencer.")
        return selection_images()
    
    #    new = I.new("RGB",(250, 250),(255,255,255))
    
    return selection_mode(img1, img2)

def selection_mode(img1, img2):
    """
    choix du mode de mélange pixel (P) ou couleur (C)

    Returns
    -------
    mode : str
        mode choisi

    """
    
    chx = str(input("Veuillez choisir le mode à utiliser: \n Pixel (P) | Couleur (C) : "))
    
    if chx == "p" or chx == "P":
        return melange_pixel(img1, img2)
    elif chx == "c" or chx == "C":
        return couleur(img1, img2)
    else:
        print("Un erreur est surveunue, veuillez recomencer.")
        return selection_mode(img1, img2)

def pixel(img1, img2):
    """
    Parameters
    ----------
    img1 : image
        image source
    img2 : image
        image source
    new : image
        image vide
    les trois images sont de mêmes dimensions

    Returns
    -------
    new : image
        melange des deux images sources
    """
    
    nb = int(input("Veuillez choisir le taux de mélange (0,100) : "))
    alpha = max(0, min(100, nb)) / 100.0

    im1 = I.open(img1).convert("RGB")
    im2 = I.open(img2).convert("RGB")

    w, h = min(im1.width, im2.width), min(im1.height, im2.height)
    im1 = im1.crop((0, 0, w, h))
    im2 = im2.crop((0, 0, w, h))

    new = I.blend(im1, im2, alpha)
    return new

def couleur(img1, img2):
    """
    Parameters
    ----------
    img1 : image
        image source
    img2 : image
        image source
    new : image
        image vide
    les trois images sont de mêmes dimensions

    Returns
    -------
    new : image
        melange des deux images sources
    """
    im1 = I.open(img1).convert("RGB")
    im2 = I.open(img2).convert("RGB")

    w, h = min(im1.width, im2.width), min(im1.height, im2.height)
    im1 = im1.crop((0, 0, w, h))
    im2 = im2.crop((0, 0, w, h))

    # Construire un masque binaire à partir de im1 en niveaux de gris
    gray = im1.convert("L")
    mask = gray.point(lambda p: 255 if p >= 128 else 0)

    new = I.composite(im1, im2, mask)
    return new

def enregistre(new):
    """
    enregistre l'image crée dans le réperoire de travail

    Parameters
    ----------
    new : image
        
    Returns
    -------
    None.

    """
    nom = input("Nom du fichier de sortie (ex: resultat.png) : ").strip() or "resultat.png"
    new.save(nom)
    print(f"Image enregistrée sous {nom}")

def afficher_image(im):
    """Affiche l'image :
    - en couleurs dans le terminal (ANSI 24-bit) si stdout est un TTY
    - via IPython.display sinon (Notebook/Jupyter)
    """
    # Si on est en terminal, utiliser un rendu couleur ANSI
    try:
        if sys.stdout.isatty():
            try:
                cols = shutil.get_terminal_size((80, 24)).columns
            except Exception:
                cols = 80
            max_width = max(10, min(cols, 120))

            rgb = im.convert("RGB")
            w, h = rgb.size
            if w == 0 or h == 0:
                print("Image vide.")
                return

            new_w = min(max_width, w)
            aspect = h / w
            new_h = max(1, int(aspect * new_w * 0.5))

            rgb = rgb.resize((new_w, new_h), resample=I.BILINEAR)
            pixels = rgb.load()

            reset = "\x1b[0m"
            for y in range(new_h):
                line_parts = []
                for x in range(new_w):
                    r, g, b = pixels[x, y]
                    line_parts.append(f"\x1b[38;2;{r};{g};{b}m█")
                line_parts.append(reset)
                print("".join(line_parts))
            print(reset, end="")
            return
    except Exception:
        # Si quelque chose échoue, on tombera sur l'affichage IPython ci-dessous
        pass

    # Sinon, tenter l'affichage via IPython.display (Notebook)
    try:
        clear_output(wait=True)
    except Exception:
        pass
    try:
        display(im)
    except Exception:
        print("Aperçu indisponible.")

def melange_pixel(img1, img2):
    while True:
        try:
            step = int(input("Taille du motif (1 pour 1 pixel sur 2, 2 pour blocs 2x2, etc.) : "))
        except Exception:
            step = 1
        if step <= 0:
            step = 1
        
        im1 = I.open(img1).convert("RGB")
        im2 = I.open(img2).convert("RGB")

        w, h = min(im1.width, im2.width), min(im1.height, im2.height)
        im1 = im1.crop((0, 0, w, h))
        im2 = im2.crop((0, 0, w, h))

        new = I.new("RGB", (w, h))
        p1 = im1.load()  # accès direct aux pixels
        p2 = im2.load()
        pn = new.load()

        for y in range(h):
            for x in range(w):
                # step=1 => damier 1 pixel sur 2
                # step=2 => damier par blocs 2x2 (un pixel sur 4 au sens “blocs”)
                if ((x // step) + (y // step)) % 2 == 0:
                    pn[x, y] = p1[x, y]
                else:
                    pn[x, y] = p2[x, y]

        afficher_image(new)

        # Satisfaction
        sat = input("Êtes-vous satisfait ? (O/N) : ").strip().lower()
        if sat in ("o", "oui", "y", "yes"):
            save = input("Voulez-vous enregistrer la nouvelle image ? (O/N) : ").strip().lower()
            if save in ("o", "oui", "y", "yes"):
                enregistre(new)
            return new
        else:
            retry = input("Voulez-vous essayer un nouveau mélange (Pixel) ? (O/N) : ").strip().lower()
            if retry not in ("o", "oui", "y", "yes"):
                return new

