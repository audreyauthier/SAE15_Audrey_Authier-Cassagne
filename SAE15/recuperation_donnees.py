# --- Importations des modules ---

import os
import requests
import json
import time


# --- Fonctions générales ---


def obtenir_donnees(url):
    """
    Fonction qui effectue une requête HTTP GET pour récupérer les données depuis une API et les retourne sous forme JSON.
    """
    response = requests.get(url)
    return response.json()


def creer_dossier_si_necessaire(chemin_dossier):
    """
   Fonction qui vérifie et crée un dossier si nécessaire.
    """
    if not os.path.exists(chemin_dossier):
        os.makedirs(chemin_dossier)


def sauvegarder_donnees_json(dossier, fichier, donnees):
    """
   Fonction qui sauvegarde les données dans un fichier JSON dans le dossier spécifié.
    """
    creer_dossier_si_necessaire(dossier)
    chemin_complet = os.path.join(dossier, fichier)
    with open(chemin_complet, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)


# --- Suivi des parkings ---


def suivre_tous_les_parkings_voitures(url, intervalle, duree, dossier, fichier):
    """
   Fonction suivant l'occupation de tous les parkings voitures.
    """
    temps_debut = time.time()
    donnees_completes = []
    while time.time() - temps_debut < duree:
        donnees = obtenir_donnees(url)
        horodatage = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        for parking in donnees:
            nom_parking = parking.get('name', {}).get('value', 'Inconnu')
            places_libres = parking.get('availableSpotNumber', {}).get('value', 'Inconnu') #places libres d'utilisation (donc ici de places disponibles pour se garer)
            capacite_totale = parking.get('totalSpotNumber', {}).get('value', 'Inconnu')
            location = parking.get('location', {}).get('value', {}).get('coordinates', [None, None])
            donnees_completes.append({
                "Horodatage": horodatage,
                "Nom parking": nom_parking,
                "Places libres": places_libres,
                "Capacite totale": capacite_totale,
                "Coordonnees": location #ajouté a posteriori pour étudier la proximité des parkings
            })
        time.sleep(intervalle)
    sauvegarder_donnees_json(dossier, fichier, donnees_completes)


def suivre_tous_les_parkings_velo(url, intervalle, duree, dossier, fichier):
    """
   Fonction suivant l'utilisation de tous les parkings vélos.
    """
    temps_debut = time.time()
    donnees_completes = []
    while time.time() - temps_debut < duree:
        donnees = obtenir_donnees(url)
        horodatage = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        for parking in donnees:
            nom_parking = parking.get('address', {}).get('value', {}).get('streetAddress', 'Inconnu')
            places_libres = parking.get('availableBikeNumber', {}).get('value', 'Inconnu') #places libres d'utilisation (donc ici de vélos disponibles à la location)
            capacite_totale = parking.get('totalSlotNumber', {}).get('value', 'Inconnu')
            location = parking.get('location', {}).get('value', {}).get('coordinates', [None, None])
            donnees_completes.append({
                "Horodatage": horodatage,
                "Nom parking velo": nom_parking,
                "Velos disponibles": places_libres,
                "Capacite totale": capacite_totale,
                "Coordonnees": location #ajouté a posteriori pour étudier la proximité des parkings
            })
        time.sleep(intervalle)
    sauvegarder_donnees_json(dossier, fichier, donnees_completes)


# --- Fonction principale ---


def main():
    """
   Fonction principal pour collecter les données des parkings voitures et vélos.
    """
    intervalle = int(input("Entrez l'intervalle d'échantillonnage (en secondes) : "))
    duree = int(input("Entrez la durée totale d'acquisition (en secondes) : "))

    # Dossiers pour les données
    dossier_voitures = "C:/Users/audre/OneDrive/Bureau/données_parkings/données_voitures"
    dossier_velos = "C:/Users/audre/OneDrive/Bureau/données_parkings/données_vélos"

    # Noms des fichiers
    fichier_voitures = "donnees_parkings_voitures.json"
    fichier_velos = "donnees_parkings_velos.json"

    # URLS des données (API)
    url_voitures = "https://portail-api-data.montpellier3m.fr/offstreetparking?limit=1000"
    url_velos = "https://portail-api-data.montpellier3m.fr/bikestation?limit=1000"

    # Suivi des parkings voitures et vélos en parallèle
    from threading import Thread

    thread_voitures = Thread(target=suivre_tous_les_parkings_voitures, args=(url_voitures, intervalle, duree, dossier_voitures, fichier_voitures))
    thread_velos = Thread(target=suivre_tous_les_parkings_velo, args=(url_velos, intervalle, duree, dossier_velos, fichier_velos))

    thread_voitures.start()
    thread_velos.start()

    thread_voitures.join()
    thread_velos.join()

# Lancer cette fonction principale
if __name__ == "__main__":
    main()
