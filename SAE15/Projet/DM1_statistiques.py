import numpy as np
import math
import matplotlib.pyplot as plt

# fonction permettant de calculer la moyenne d'une liste de nombres
def moyenne (tableau):
    accumulateur=0
    for i in range(len(tableau)):
        accumulateur = accumulateur+tableau[i]
    return accumulateur/len(tableau)

# fonction permettant de calculer la variance d'une liste de nombres
def variance (tableau):
    accumulateur=0
    moy=moyenne(tableau)
    for i in range(len(tableau)):
        accumulateur = accumulateur+(tableau[i]-moy)**2
    return accumulateur/len(tableau)

# fonction permettant de calculer l'écart type (sigma) d'une liste de nombres
def ecart_type(tableau):
    var=variance(tableau)
    return math.sqrt(var)

# fonction permettant de calculer la covariance entre deux listes de nombres
def covariance(tableau1, tableau2):
    accumulateur=0
    moy_tableau1=moyenne(tableau1)
    moy_tableau2=moyenne(tableau2)
    for i in range(len(tableau1)):
        accumulateur=accumulateur+(tableau1[i]-moy_tableau1)*(tableau2[i]-moy_tableau2)
    return accumulateur/len(tableau1)

# fonction permettant de calculer le coefficient de corrélation entre deux listes de nombres
def correlation(tableau1, tableau2):
    ecart_type1=ecart_type(tableau1)
    ecart_type2=ecart_type(tableau2)
    return covariance(tableau1,tableau2)/(ecart_type1*ecart_type2)

# fonction permettant de calculer la matrice de corrélation 
# (de taille NxN) entre N listes de nombres
def matrice_correlation(all_data) :
    N = len(all_data)
    resultat = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            resultat[i][j]=correlation(all_data[i],all_data[j])
    return resultat

def affiche_grille (liste):
    for i in range(len(liste)):
        print(' | '.join(map(str,liste[i])))

#fonction permettant de représenter l'évolution d'une grandeur (graphique)
def afficher_evolution(instants, valeurs, titre="Évolution d'une grandeur", xlabel="Temps (en h)", ylabel="Valeur", nom_courbe="Courbe"):
    plt.figure(figsize=(10, 6))
    plt.plot(instants, valeurs, marker='x', linestyle='-', label=nom_courbe, color='hotpink')
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xlim(0,23)
    plt.xticks(range(0, 24, 1))
    plt.legend()
    plt.show()

#fonction permettant de représenter graphiquement (par une heatmap) les corrélations entre N listes de nombres
def afficher_heatmap_correlation(matrice):
    plt.figure(figsize=(6, 6))
    plt.imshow(matrice, cmap='Purples', interpolation='nearest')
    plt.colorbar(label="Coefficient de corrélation")
    plt.title("Heatmap des corrélations")
    plt.xticks(np.arange(3), ['Salle 1', 'Salle 2', 'Temps'])
    plt.yticks(np.arange(3), ['Salle 1', 'Salle 2', 'Temps'])
    plt.show()

#Vérifications

#T=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
#L1=[3,3,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,8,7,4]
#L2=[103,203,4,3,2,5,8,9,13,16,18,18,19,21,22,22,21,17,17,12,10,-92,-93,-96]

#print(f'La moyenne de L1 est : {moyenne(L1)}')
#print(f'L\'écart type (ou sigma) de L1 est : {ecart_type(L1):.2f}\n')

#print(f'La moyenne de L2 est : {moyenne(L2)}')
#print(f'L\'écart type (ou sigma) de L2 est : {ecart_type(L2):.2f}\n')

# print('Matrice de corrélation:')
# affiche_grille(matrice_correlation([L1,L2,T]))

# afficher_evolution(T, L1, titre="Évolution de la température en fonction du temps (Salle 1)", ylabel="Température (en °C)", nom_courbe="L1")
# afficher_evolution(T, L2, titre="Évolution de la température en fonction du temps (Salle 2)", ylabel="Température (en °C)", nom_courbe="L2")

# afficher_heatmap_correlation(matrice_correlation([L1, L2, T]))