# SAE15_Audrey_Authier-Cassagne

**Mon projet est disponible ici**:  
[Mobilité dans Montpellier et son agglomération: une étude de l'utilisation des parkings et du relais voiture/vélo](https://audreyauthier.github.io/SAE15_Audrey_Authier-Cassagne/)


NB: Une explication de l'arborescence des fichiers présents sur ce dépôt est présente tout en bas de cette page.

-----
# Genèse de mon projet

Dans le cadre de ma formation en **BUT Réseaux et Télécommunications**, j'ai été mandatée par la mairie de Montpellier pour réaliser une étude sur l’utilisation des parkings de la ville, dans le cadre de la **SAE 15**. Cette étude avait pour but de répondre à plusieurs questions concernant les parkings voitures et vélos, en particulier sur leur taux d'occupation et la relation entre l’utilisation des parkings de véhicules et de vélos. Le projet visait également à analyser si ces parkings étaient bien dimensionnés et à observer les corrélations potentielles entre les parkings pour mieux comprendre leur utilisation.

## 1. Mise en Situation et Objectifs du Projet

Le maire de Montpellier m’a mandaté pour étudier l’occupation des parkings de la ville, en particulier :

- Le taux d’occupation des parkings voitures et le taux d'utilisation des vélos.
- L’analyse de la relation entre l’utilisation des parkings de voitures et de vélos, pour voir s’il existait des liens entre l’utilisation des parkings voitures et la location des vélos dans les parkings vélos situés à proximité.

L’objectif principal était de déterminer si les parkings étaient bien dimensionnés et de vérifier si des corrélations existent entre l'usage des parkings voitures et vélos, en tenant compte de leur proximité géographique.

## 2. Collecte des Données

Pour ce projet, j’ai récupéré les données publiques concernant les parkings de la ville, via le portail **API du site Open Data de Montpellier**. Voici les données spécifiques que j’ai récupérées pour chaque type de parking :

### Pour les parkings vélos :
- **Horodatage** : `"2024-12-31 23:20:01"`
- **Nom parking vélo** : `"Rue Jules Ferry - Gare Saint-Roch"`
- **Vélos disponibles** : 4
- **Capacité totale** : 12

### Pour les parkings voitures :
- **Horodatage** : `"2024-12-31 23:20:01"`
- **Nom parking** : `"Antigone"`
- **Places libres** : 162
- **Capacité totale** : 239

Ces données ont été collectées sur une période de **7 jours** (du 26 décembre 2024 au 1er janvier 2025), à intervalle de 5 minutes. Mon analyse s'est principalement concentrée sur les heures entre **6h et 22h** pour évaluer la fréquentation des parkings.

## 3. Collecte des Coordonnées des Parkings (Proximité)

Afin de pouvoir analyser la proximité géographique des parkings, il m’a fallu récupérer les coordonnées géographiques (**latitude** et **longitude**) des parkings voitures et vélos.

- J’ai récupéré ces coordonnées GPS en quelques secondes pour chaque parking, tant pour les parkings voitures que pour les parkings vélos.
- Ces coordonnées étaient nécessaires pour mesurer la distance géographique entre les parkings et établir leur relation de proximité.

# 4. Traitement des Données

Après avoir récupéré les données nécessaires, j’ai procédé à leur traitement pour calculer les taux d’occupation des parkings. Cependant, en raison de la différence de nature des parkings (voitures et vélos), les calculs ont été adaptés :

## Parkings voitures

Pour les parkings voitures, le **taux d'occupation** est calculé comme suit :

$$
\text{Taux d'occupation du parking voitures \%} = \frac{\text{Nombre de places occupées}}{\text{Capacité totale}} \times 100
$$

Or, sur le site, j’ai récupéré le **nombre de places libres d'utilisation**. Donc :

$$
\text{Nombre de places occupées} = \text{Capacité totale} - \text{Nombre de places libres d'utilisation}
$$

Ainsi :

$$
\text{Taux d'occupation du parking voitures \%} = \frac{\text{Capacité totale} - \text{Nombre de places libres d'utilisation}}{\text{Capacité totale}} \times 100
$$

Ce qui revient à :

$$
\text{Taux d'occupation du parking voitures \%} = 1 - \frac{\text{Nombre de places libres d'utilisation}}{\text{Capacité totale}} \times 100
$$

---

## Parkings vélos

Pour les parkings vélos, le **taux d’utilisation** est calculé de manière similaire :

$$
\text{Taux d'occupation ou d'utilisation vélos \%} = \frac{\text{Nombre de vélos utilisés}}{\text{Capacité totale}} \times 100
$$

Or, sur le site, j’ai récupéré le **nombre de vélos disponibles** (non utilisés = places libres d'utilisation). Donc :

$$
\text{Nombre de vélos utilisés} = \text{Capacité totale} - \text{Nombre de places libres d'utilisation}
$$

Ainsi :

$$
\text{Taux d'occupation ou d'utilisation vélos \%} = \frac{\text{Capacité totale} - \text{Nombre de places libres d'utilisation}}{\text{Capacité totale}} \times 100
$$

Ce qui revient à :

$$
\text{Taux d'occupation ou d'utilisation vélos \%} = 1 - \frac{\text{Nombre de places libres d'utilisation}}{\text{Capacité totale}} \times 100
$$  

Cela signifie qu’un parking avec peu de vélos disponibles est plus utilisé et a donc un taux d'utilisation plus important.

J’ai ensuite organisé les données pour permettre une analyse journalière et statistique. J’ai ainsi généré des graphiques pour visualiser ces taux sur plusieurs jours.

---

# 5. La Proximité des Parkings et la Heatmap des Corrélations

Avant de générer la heatmap des corrélations, il m’a fallu déterminer la proximité géographique des parkings. J'ai estimé qu’une distance de **500 mètres** (environ 5 minutes à pied) serait raisonnable pour analyser la proximité des parkings vélos aux parkings voitures, et vice versa.

Pour cela, j'ai calculé la distance géographique entre les parkings en utilisant leurs coordonnées GPS. J'ai choisi cette distance de 500 mètres en me basant sur une estimation réaliste de la distance qu'une personne pourrait parcourir entre un parking vélo et un parking voiture.

Ensuite, j'ai créé un tableau des parkings proches, c’est-à-dire des parkings vélos situés à moins de 500 mètres d’un parking voiture, et inversement. Cela m’a permis de filtrer les corrélations de la heatmap pour ne garder que les parkings dont la proximité géographique était significative.

Sans ce tableau, la heatmap incluait des corrélations entre des parkings qui étaient géographiquement proches, mais pas nécessairement corrélés en termes d'utilisation. Par exemple, deux parkings peuvent être proches sans que leurs taux d’occupation soient liés. Le tableau des parkings proches a donc permis de mieux interpréter la heatmap en filtrant les corrélations non pertinentes.

---

# 6. Les Graphiques et Défis Techniques

Afin de rendre les résultats accessibles, j’ai créé plusieurs types de graphiques :

- **Graphiques des taux d'occupation** pour les parkings voitures et **taux d'utilisation** pour les parkings vélos.
- **Graphiques des écarts-types de l’occupation ou de l'utilisation** des parkings sous forme de barres.
- **Heatmap des corrélations**, où les parkings proches étaient mis en évidence.
- **Tableaux récapitulatifs**, contenant des informations comme les moyennes des taux d'occupation ou d’utilisation et les écarts-types.

### Défis rencontrés
Le principal défi que j’ai rencontré était de garder mes graphiques interactifs. Au début, je souhaitais utiliser matplotlib, car c’était ce qui m’avait été demandé, mais j'ai rencontré un problème pour ajouter une légende lisible à mes graphiques, notamment en raison du grand nombre de parkings (57 parkings vélos et 24 parkings voitures). Le problème était que les légendes étaient trop grandes et difficiles à intégrer proprement.
J’ai donc décidé de passer à Plotly pour créer des graphiques interactifs. Avec Plotly, j’ai pu créer des graphes interactifs et ajouter des informations supplémentaires en utilisant la fonction de survol. Cela a rendu les graphiques beaucoup plus lisibles, même avec un grand nombre de courbes.

Cependant, quand j’ai tenté d’exporter mes résultats depuis Jupyter Notebook mais aussi Google Colab, j’ai rencontré un autre problème : ces plateformes génèrent des fichiers HTML statiques qui ne permettent pas d’afficher les graphiques interactifs. C’est pourquoi j’ai utilisé Google Colab pour enregistrer mes graphiques au format HTML, puis j’ai intégré les graphiques et les tableaux dans une page web HTML que j’ai moi même codé puis hébergée sur GitHub.

---

# 7. La Création de la Page Web

Pour héberger mes résultats sur GitHub, j’ai décidé de coder ma propre page HTML. Cela m’a permis de centraliser tous mes résultats (graphiques interactifs, tableaux, heatmap) et de les rendre accessibles sous forme de page web. J’ai pris soin de bien organiser cette page pour que les différents graphiques et tableaux soient faciles à consulter, tout en expliquant clairement les résultats obtenus.

J'ai intégré mes graphismes interactifs exportés en HTML (pour les parkings vélos et voitures), mes graphiques en barres pour les écarts-types, et mes tableaux HTML directement dans la page, tout en expliquant chaque étape de l’analyse et les résultats principaux. Cela m’a permis de répondre efficacement à la demande du maire de la ville de Montpellier.

---

# 8. Conclusion

En conclusion, ce projet m’a permis de développer des compétences en collecte et traitement de données, analyse statistique, et visualisation graphique. J’ai étudié l’utilisation des parkings de la ville de Montpellier, analysé la relation entre l'occupation des parkings voitures et vélos, et créé des graphes et des tableaux récapitulatifs pour présenter mes résultats.
Ce travail m’a également permis d’apprendre à résoudre des problèmes techniques liés à la création de graphiques interactifs et à l’intégration de résultats dans une page HTML. Le projet a été finalisé sur une page web hébergée sur GitHub,pour conserver la synthèse de mon analyse de ces données pour la rendre accessible au maire de Montpellier et aux parties prenantes.

---
---

## Structure du dépôt

### 1. Dossier `HTMLSAE15`
Ce dossier contient tous les fichiers nécessaires pour afficher le site web interactif hébergé sur GitHub Pages. 
Voici un aperçu de son contenu :

- **`graphique_velos.html`** : Graphique interactif pour les parkings vélos.
- **`graphique_voitures.html`** : Graphique interactif pour les parkings voitures.
- **`heatmap.png`** : Carte thermique des corrélations entre les parkings proches.
- **`ecart_type_velos.png`** : Graphique des écarts-types pour les parkings vélos.
- **`ecart_type_voitures.png`** : Graphique des écarts-types pour les parkings voitures.
- **Tableaux récapitulatifs** :
  - `tableau_parkings_proches`
  - `tableau_velos`
  - `tableau_voitures`

---

### 2. Dossier `SAE15`
Ce dossier contient les scripts et données pour la collecte, le traitement et l'analyse des parkings.

#### 2.1. Sous-dossier `Comparer_la_proximité_des_parkings`
- **`Comparer_proximité_parkings.py`** : Programme pour analyser la proximité géographique entre les parkings vélos et voitures.
- **`donnees_parkings_velos.json`** et **`donnees_parkings_voitures.json`** : Données brutes des parkings vélos et voitures.
- **`tableau_parkings_proches`** : Tableau des parkings considérés comme proches (≤ 500 m).
- **`parkings_voitures_velos_proches.json`** : Liste des parkings avec proximité confirmée.

#### 2.2. Sous-dossier `Graphiques_tableaux`
Ce dossier contient les graphiques et tableaux générés :
- Graphiques des taux d'occupation et écarts-types (format PNG et HTML).
- Tableaux synthétiques des données.

#### 2.3. Sous-dossier `Projet`
- **`DM1_statistiques.py`** : Fichier Python contenant des fonctions statistiques de base utilisées dans le projet.

#### 2.4. Sous-dossiers `velos` et `voitures`
Ces dossiers contiennent les fichiers JSON bruts pour les données de parkings vélos et voitures sur 7 jours (du 26 décembre au 1er janvier).

---

### 3. Scripts principaux
Voici une liste des scripts clés utilisés dans mon projet :

- [Comparer la proximité des parkings](SAE15/Comparer_la_proximité_des_parkings/Comparer_proximité_parkings.py)  
  Analyse la proximité géographique entre les parkings vélos et voitures.
- [Récupération des données](SAE15/recuperation_donnees.py)  
  Programme pour collecter les données brutes via l'API Open Data de Montpellier.
- [Traitement des données](SAE15/programmes_traitement_donnees.py)  
  Script pour calculer les taux d'occupation et générer les graphiques.

---

## Accéder aux données
Les données brutes et résultats sont accessibles via les sous-dossiers dans `SAE15`.

---


