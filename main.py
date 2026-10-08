#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ZACKARY ESTEVES | BAPTISTE DEVEAUX DE MARIGNY | NSI GROUPE RAJABALEE
BY-NC 4.0   (vous pouvez changer la licence, pour choisir une licence libre : https://creativecommons.org/choose/?lang=fr)
"""

############################################
#          IMPORTATION DES MODULES         #
# Vous pouvez bien sur en utiliser d'autre #
############################################

import fonctions as f
from PIL import Image as img
import shutil

# Pour l'instant les fonctions disponibles ne retournent pas le bon résultat mais
# elles vous permettent de commencer à travailler sur le programme principal.
        
#########################################
# LE CORPS PRINCIPAL DE VOTRE PROGRAMME #
#########################################

def afficher_image_terminal(im, max_width=None):
    """Affiche l'image en couleurs (ANSI 24-bit) dans le terminal."""
    # Largeur du 
    try:
        cols = shutil.get_terminal_size((80, 24)).columns
    except Exception:
        cols = 80
    if max_width is None:
        max_width = max(10, min(cols, 120))

    rgb = im.convert("RGB")
    w, h = rgb.size
    if w == 0 or h == 0:
        print("Image vide.")
        return

    new_w = min(max_width, w)
    aspect = h / w
    new_h = max(1, int(aspect * new_w * 0.5))

    rgb = rgb.resize((new_w, new_h), resample=img.BILINEAR)
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


def main():
    new = f.selection_images()
    if new != None:
        afficher_image_terminal(new)
    else:
        print("Aucune image générée.")


if __name__ == "__main__":
    main()