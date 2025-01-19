# --- Importations des modules ---

from Projet.DM1_statistiques import variance, moyenne, ecart_type, covariance
import os
import json
import datetime as dt
import random
import numpy as np
from tabulate import tabulate
from collections import defaultdict
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# --- Fonctions de base pour calculs statistiques et corrélation car un peu différent de celle dans le DM1 ---


def correlation(tableau1, tableau2):
    ecart_type1 = ecart_type(tableau1)
    ecart_type2 = ecart_type(tableau2)
    if ecart_type1 == 0 or ecart_type2 == 0:
        return 0  # Pas de corrélation possible
    return covariance(tableau1, tableau2) / (ecart_type1 * ecart_type2)


# --- Fonctions pour le traitement des données ---


def filtrer_par_horaires(donnees, heure_debut=6, heure_fin=22):
    """
    Filtre les données pour ne conserver que celles entre les heures spécifiées.
    """
    donnees_filtrees = []
    for entree in donnees:
        horodatage = dt.datetime.strptime(entree["Horodatage"], "%Y-%m-%d %H:%M:%S")
        if heure_debut <= horodatage.hour <= heure_fin:
            donnees_filtrees.append(entree)
    return donnees_filtrees


def calculer_taux_occupation(donnees, type_parking):
    """
    Calcule le taux d'occupation pour chaque entrée de données.
    """
    for entree in donnees:
        capacite = entree["Capacite totale"]
        places_libres_d_utilisation = entree["Places libres" if type_parking == "voiture" else "Velos disponibles"]
        if capacite != "Inconnu" and capacite > 0:
            entree["Taux d'occupation (%)"] = (1 - places_libres_d_utilisation / capacite) * 100


def regrouper_par_jour(donnees):
    """
    Regroupe les données par jour.
    """
    donnees_par_jour = {}
    for entree in donnees:
        horodatage = dt.datetime.strptime(entree["Horodatage"], "%Y-%m-%d %H:%M:%S")
        jour = horodatage.date()
        if jour not in donnees_par_jour:
            donnees_par_jour[jour] = []
        donnees_par_jour[jour].append(entree)
    return donnees_par_jour


def charger_tous_les_fichiers(repertoire, type_parking):
    """
    Charge tous les fichiers JSON d'un répertoire et calcule les taux d'occupation (ou d'utilisation pour les vélos).
    """
    all_data = {}
    for fichier in os.listdir(repertoire):
        if fichier.endswith(".json"):
            with open(os.path.join(repertoire, fichier), "r", encoding="utf-8") as f:
                donnees = json.load(f)
                donnees_filtrees = filtrer_par_horaires(donnees)
                calculer_taux_occupation(donnees_filtrees, type_parking)
                for entree in donnees_filtrees:
                    nom = entree["Nom parking" if type_parking == "voiture" else "Nom parking velo"]
                    if nom not in all_data:
                        all_data[nom] = []
                    all_data[nom].append(entree)
    return all_data


# --- Fonctions pour l'analyse statistique ---


def calculer_statistiques_parking(all_data):
    """
    Calcule les statistiques de chaque parking : moyenne, variance, écart-type.
    """
    stats = {}
    for nom_parking, donnees in all_data.items():
        taux_occupation = [entree["Taux d'occupation (%)"] for entree in donnees]
        stats[nom_parking] = {
            "Moyenne": moyenne(taux_occupation),
            "Variance": variance(taux_occupation),
            "Écart-Type": ecart_type(taux_occupation)
        }
    return stats


def calculer_moyenne_horaire(donnees):
    """
    Calcule la moyenne horaire des taux d'occupation pour chaque heure de la journée.
    """
    heures = defaultdict(list)
    for entree in donnees:
        horodatage = dt.datetime.strptime(entree["Horodatage"], "%Y-%m-%d %H:%M:%S")
        heure = horodatage.hour
        if 6 <= heure <= 22:
            taux_occupation = entree["Taux d'occupation (%)"]
            heures[heure].append(taux_occupation)

    moyennes_horaires = {heure: moyenne(valeurs) for heure, valeurs in heures.items()}
    return moyennes_horaires


def calculer_matrice_correlation(donnees_voitures, donnees_velos):
    """
    Calcule la matrice de corrélation entre l'usage des parkings voitures et les vélos.
    """
    noms_voitures = list(donnees_voitures.keys())
    noms_velos = list(donnees_velos.keys())

    # Stocker les moyennes horaires pour chaque parking
    donnees_moyennes = {}

    for nom in noms_voitures:
        moyennes_horaires = calculer_moyenne_horaire(donnees_voitures[nom])
        donnees_moyennes[nom] = [moyennes_horaires.get(heure, 0) for heure in range(6, 23)]

    for nom in noms_velos:
        moyennes_horaires = calculer_moyenne_horaire(donnees_velos[nom])
        donnees_moyennes[nom] = [moyennes_horaires.get(heure, 0) for heure in range(6, 23)]

    # Créer la matrice de corrélation
    noms_parkings = list(donnees_moyennes.keys())
    matrice_corr = np.zeros((len(noms_voitures), len(noms_velos)))

    for i, nom_voiture in enumerate(noms_voitures):
        for j, nom_velo in enumerate(noms_velos):
            taux_voiture = donnees_moyennes[nom_voiture]
            taux_velo = donnees_moyennes[nom_velo]
            matrice_corr[i, j] = correlation(taux_voiture, taux_velo)

    return noms_voitures, noms_velos, matrice_corr


# --- Fonctions pour l'affichage des données ---


def afficher_graphique_par_jour(all_data, titre="Taux d'occupation par parking", fichier_html="graphique.html"):
    """
    Affiche un graphique interactif du taux d'occupation (ou d'utilisation) par jour pour chaque parking.
    """
    jours_data = []
    moyennes_data = []
    parkings_data = []

    for nom_parking, donnees in all_data.items():
        donnees_par_jour = regrouper_par_jour(donnees)
        jours = sorted(donnees_par_jour.keys())
        moyennes_par_jour = []

        for jour in jours:
            taux_jour = [entree["Taux d'occupation (%)"] for entree in donnees_par_jour[jour]]
            moyenne_jour = moyenne(taux_jour)
            moyennes_par_jour.append(moyenne_jour)

        parkings_data.extend([nom_parking] * len(jours))
        jours_data.extend(jours)
        moyennes_data.extend(moyennes_par_jour)

    fig = go.Figure()

    # Ajout d'une courbe pour chaque parking
    for nom_parking in set(parkings_data):
        indices = [i for i, x in enumerate(parkings_data) if x == nom_parking]
        fig.add_trace(go.Scatter(
            x=[jours_data[i] for i in indices],
            y=[moyennes_data[i] for i in indices],
            mode='lines+markers',
            marker=dict(symbol='x', size=5),
            text=[nom_parking] * len(indices),
            line=dict(width=0.8),
            showlegend=False,
            hoverinfo='text',
            hovertemplate='<b>%{text}</b><br>Taux: %{y:.2f}%<extra></extra>'
        ))

    # Mettre à jour le titre et les étiquettes
    fig.update_layout(
        title=titre,
        xaxis_title="Jours",
        yaxis_title="Taux moyen (en %)",
        hovermode="closest"
    )

    # Sauvegarder et afficher le graphique
    fig.write_html(f"C:/Users/audre/OneDrive/Bureau/SAE15/Graphiques_tableaux/{fichier_html}")
    fig.show()


def afficher_ecart_type(stats, titre="Écart-type des taux d'occupation par parking", fichier_image="ecart_type.png"):
    """
    Affiche un graphique en barres des écarts-types des taux d'occupation ou d'utilisation par parking.
    """
    parkings = list(stats.keys())
    ecarts = [stats[parking]["Écart-Type"] for parking in parkings]
    couleurs = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in parkings]

    plt.figure(figsize=(15, 7))
    plt.bar(parkings, ecarts, color=couleurs)
    plt.title(titre)
    plt.xlabel("Parkings")
    plt.ylabel("Écart-Type (en %)")
    plt.xticks(rotation=90, ha="center", fontsize=8)
    plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.savefig(f"C:/Users/audre/OneDrive/Bureau/SAE15/Graphiques_tableaux/{fichier_image}")
    plt.show()


def afficher_heatmap(noms_voitures, noms_velos, matrice_corr):
    """
    Affiche une heatmap des corrélations entre parkings voitures et vélos.
    """
    plt.figure(figsize=(12, 10))
    im = plt.imshow(matrice_corr, cmap="coolwarm", interpolation="nearest")
    plt.colorbar(im, label="Coefficient de corrélation")
    plt.xticks(range(len(noms_velos)), noms_velos, rotation=90, fontsize=9)
    plt.yticks(range(len(noms_voitures)), noms_voitures, fontsize=9)
    plt.xlabel("Noms des parkings vélos", fontsize=10, labelpad=20)
    plt.ylabel("Noms des parkings voitures", fontsize=10, labelpad=20)
    plt.title("Heatmap des corrélations entre les parkings voitures et vélos", fontsize=13, pad=25)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.4, top=0.9, left=0.25, right=0.95)
    plt.savefig(f"C:/Users/audre/OneDrive/Bureau/SAE15/Graphiques_tableaux/heatmap.png")
    plt.show()


def afficher_tableau_recapitulatif_velos(stats, titre="Tableau récapitulatif des parkings vélos"):
    """
    Affiche et enregistre un tableau récapitulatif pour les parkings vélos (taux d'utilisation moyen et écart-type)
    """
    tableau = []
    for nom_parking, valeurs in stats.items():
        tableau.append([
            nom_parking,
            f"{valeurs['Moyenne']:.2f} %",
            f"{valeurs['Écart-Type']:.2f} %",
        ])

    print(f"\n{titre}\n")
    print(tabulate(tableau, headers=["Parking", "Moyenne taux d'occupation (en %)", "Écart-Type des taux d'utilisation (en %)"], tablefmt="fancy_grid", numalign='center'))

    tableau_html = tabulate(tableau, headers=["Parking", "Moyenne taux d'occupation (en %)", "Écart-Type des taux d'utilisation (en %)"], tablefmt="html")
    with open(f"C:/Users/audre/OneDrive/Bureau/SAE15/Graphiques_tableaux/tableau_velos", "w") as f:
      f.write(tableau_html)


def afficher_tableau_recapitulatif_voitures(stats, titre="Tableau récapitulatif des parkings voitures"):
    """
    Affiche et enregistre un tableau récapitulatif pour les parkings voiture (taux d'occupation moyen et écart-type)
    """
    tableau = []
    for nom_parking, valeurs in stats.items():
        tableau.append([
            nom_parking,
            f"{valeurs['Moyenne']:.2f} %",
            f"{valeurs['Écart-Type']:.2f} %"
        ])

    print(f"\n{titre}\n")
    print(tabulate(tableau, headers=["Parking", "Moyenne taux d'occupation (en %)", "Écart-Type des taux d'occupation (en %)"], tablefmt="fancy_grid", numalign='center'))

    tableau_html = tabulate(tableau, headers=["Parking", "Moyenne taux d'occupation (en %)", "Écart-Type des taux d'occupation (en %)"], tablefmt="html")
    with open(f"C:/Users/audre/OneDrive/Bureau/SAE15/Graphiques_tableaux/tableau_voitures", "w") as f:
        f.write(tableau_html)


# --- Traitement et affichage ---

# Chemin des répertoires contenant les fichiers JSON
repertoire_voitures = "C:/Users/audre/OneDrive/Bureau/SAE15/voitures"
repertoire_velos = "C:/Users/audre/OneDrive/Bureau/SAE15/velos"

# Chargement des données
donnees_voitures = charger_tous_les_fichiers(repertoire_voitures, "voiture")
donnees_velos = charger_tous_les_fichiers(repertoire_velos, "velo")

# Affichage des graphiques
afficher_graphique_par_jour(donnees_voitures, titre="Taux d'occupation quotidien des parkings voitures sur 7 jours", fichier_html="graphique_voitures.html")
afficher_graphique_par_jour(donnees_velos, titre="Taux d'utilisation quotidien des vélos par parking sur 7 jours", fichier_html="graphique_velos.html")

# Calcul des statistiques et affichage de l'écart type
stats_voitures = calculer_statistiques_parking(donnees_voitures)
stats_velos = calculer_statistiques_parking(donnees_velos)

afficher_ecart_type(stats_voitures, titre="Écart-type des taux d'occupation des parkings voitures sur 7 jours", fichier_image="ecart_type_voitures.png")
afficher_ecart_type(stats_velos, titre="Écart-type des taux d'utilisation des vélos par parking sur 7 jours", fichier_image="ecart_type_velos.png")

# Affichage des tableaux récapitulatifs pour les parkings voitures et vélos
afficher_tableau_recapitulatif_velos(stats_velos, titre="Tableau récapitulatif des parkings vélos sur 7 jours")
afficher_tableau_recapitulatif_voitures(stats_voitures, titre="Tableau récapitulatif des parkings voitures sur 7 jours")

# Chargement et filtration des noms des parkings sans correspondance
fichier_blacklist = "C:/Users/audre/OneDrive/Bureau/SAE15/Comparer_la_proximité_des_parkings/parkings_sans_proximite.json"
with open(fichier_blacklist, "r", encoding="utf-8") as f:
    parkings_sans_proximite = json.load(f)
parkings_voitures_blacklist = set(parkings_sans_proximite["voitures_sans_proximite"])
parkings_velos_blacklist = set(parkings_sans_proximite["velos_sans_proximite"])

donnees_voitures_filtrees = {
    nom: donnees
    for nom, donnees in donnees_voitures.items()
    if nom not in parkings_voitures_blacklist
}
donnees_velos_filtrees = {
    nom: donnees
    for nom, donnees in donnees_velos.items()
    if nom not in parkings_velos_blacklist
}

# Calcul et affichage de la heatmap des corrélations
noms_voitures, noms_velos, matrice_corr = calculer_matrice_correlation(donnees_voitures_filtrees, donnees_velos_filtrees)
afficher_heatmap(noms_voitures, noms_velos, matrice_corr)