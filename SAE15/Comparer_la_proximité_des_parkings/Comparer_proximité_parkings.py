# --- Importations des modules ---

from math import *
import json
from tabulate import tabulate


# --- Fonctions de calcul géographique ---


def haversine(lon1, lat1, lon2, lat2):
    """
    Fonction pour calculer la distance entre deux points GPS en km (formule de Haversine)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  # Conversion en radians
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Rayon moyen de la Terre en km
    return c * r


def sont_proches(coord1, coord2):
    """
    Fonction pour vérifier si deux parkings sont proches (soit à moins de 500m ou 0,5 km)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    distance = haversine(lon1, lat1, lon2, lat2)
    return distance <= 0.5


# --- Fonctions pour le traitement des parkings ---


def comparer_parkings(parkings_voitures, parkings_velos):
    """
    Fonction pour comparer les parkings vélos et voitures (regroupe les parkings vélos proches pour chaque parking voiture)
    """
    correspondance = {}

    for nom_voiture, coord_voiture in parkings_voitures.items():
        correspondance[nom_voiture] = []
        for nom_velo, coord_velo in parkings_velos.items():
            if sont_proches(coord_velo, coord_voiture):
                distance = round(haversine(*coord_velo[::-1], *coord_voiture[::-1]), 2)
                correspondance[nom_voiture].append((nom_velo, distance))

    return correspondance


def charger_coordonnees(fichier, type_parking):
    """
    Fonction pour charger les données d'un fichier JSON et retourner un dictionnaire associant le nom des parkings à leurs coordonnées.
    """
    with open(fichier, "r", encoding="utf-8") as f:
        donnees = json.load(f)

    coordonnees = {}
    for parking in donnees:
        nom = parking.get("Nom parking" if type_parking == "voiture" else "Nom parking velo", "Inconnu")
        coords = parking.get("Coordonnees", [None, None])
        if coords != [None, None]:  # si les coordonnées existent
            coordonnees[nom] = tuple(coords)
    return coordonnees


# --- Chemins et chargement des données ---


# Chemins des fichiers JSON

fichier_voitures = "C:/Users/audre/OneDrive/Bureau/SAE15/Comparer_la_proximité_des_parkings/donnees_parkings_voitures.json"
fichier_velos = "C:/Users/audre/OneDrive/Bureau/SAE15/Comparer_la_proximité_des_parkings/donnees_parkings_velos.json"

# Chargement des données

parkings_voitures = charger_coordonnees(fichier_voitures, "voiture")
parkings_velos = charger_coordonnees(fichier_velos, "velo")


# --- Comparaison et statistiques ---


# Compter le nombre total de parkings voitures et vélos

nombre_parkings_voitures = len(parkings_voitures)
nombre_parkings_velos = len(parkings_velos)
print(f"\n{nombre_parkings_voitures} parkings voitures au total")
print(f"\n{nombre_parkings_velos} parkings vélos au total")


# Comparer les parkings et afficher puis sauvegarder les résultats sous forme de tableau

correspondance = comparer_parkings(parkings_voitures, parkings_velos)
tableau = []
for nom_voiture, parkings_proches in correspondance.items():
    for nom_velo, distance in parkings_proches:
        tableau.append([nom_voiture, nom_velo, f"{distance} km"])

print('\nLes parkings voitures et vélos à moins de 500m les uns des autres sont:\n')
print(tabulate(tableau, headers=["Parking Voiture", "Parking Vélo", "Distance"], tablefmt="fancy_grid"))

tableau_html = tabulate(tableau, headers=["Parking Voiture", "Parking Vélo", "Distance"],  tablefmt="html")
with open("C:/Users/audre/OneDrive/Bureau/SAE15/Comparer_la_proximité_des_parkings/tableau_parkings_proches", "w") as f:
    f.write(tableau_html)


# Trouver les parkings voiture et vélo sans correspondance puis afficher et sauvegarder les résultats sous forme de dictionnaire.

parkings_voiture_sans_proximite = []
for nom_voiture, coord_voiture in parkings_voitures.items():
    if nom_voiture not in correspondance or not correspondance[nom_voiture]:
        parkings_voiture_sans_proximite.append(nom_voiture)

parkings_velo_sans_proximite = []
for nom_velo, coord_velo in parkings_velos.items():
    if not any(nom_velo in [velo[0] for velo in parkings_proches] for parkings_proches in correspondance.values()):
        parkings_velo_sans_proximite.append(nom_velo)

print(f"\n\n{len(parkings_voiture_sans_proximite)}/{nombre_parkings_voitures} parkings voiture sans proximité avec un parking vélo (distance > 500m):\n")
for parking in parkings_voiture_sans_proximite:
    print(f"- {parking}")
print('\n')

print(f"{len(parkings_velo_sans_proximite)}/{nombre_parkings_velos} parkings vélo sans proximité avec un parking voiture (distance > 500m):\n")
for parking in parkings_velo_sans_proximite:
    print(f"- {parking}")
print('\n')

parkings_sans_proximite = {
    "voitures_sans_proximite": parkings_voiture_sans_proximite,
    "velos_sans_proximite": parkings_velo_sans_proximite
}

fichier_blacklist = "C:/Users/audre/OneDrive/Bureau/SAE15/Comparer_la_proximité_des_parkings/parkings_sans_proximite.json"
with open(fichier_blacklist, "w", encoding="utf-8") as f:
    json.dump(parkings_sans_proximite, f, indent=4, ensure_ascii=False)
