# SAE15_Audrey_Authier-Cassagne

Mon projet est disponible ici: https://audreyauthier.github.io/SAE15_Audrey_Authier-Cassagne/

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

Or, sur le site, j’ai récupéré le **nombre de vélos disponibles** (non utilisés = libres d'utilisation). Donc :

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

Cela signifie qu’un parking avec peu de vélos disponibles est plus utilisé, et donc plus occupé.

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

- **Graphiques des taux d'occupation et d'utilisation** pour les parkings voitures et vélos.
- **Graphiques des écarts-types** de l’occupation des parkings sous forme de barres.
- **Heatmap des corrélations**, où les parkings proches étaient mis en évidence.
- **Tableaux récapitulatifs**, contenant des informations comme les moyennes des taux d’utilisation et les écarts-types.

### Défis rencontrés
1. **Légendes difficiles à intégrer :**  
   Avec matplotlib, la grande quantité de données (57 parkings vélos et 24 parkings voitures) rendait les légendes illisibles.

   **Solution :**  
   J’ai opté pour Plotly, qui permet de créer des graphiques interactifs avec des fonctions de survol pour afficher des informations supplémentaires.

2. **Exportation des graphiques interactifs :**  
   Jupyter Notebook et Google Colab génèrent des fichiers HTML statiques qui ne permettent pas d’afficher les graphiques interactifs.

   **Solution :**  
   J’ai exporté les graphiques au format HTML, puis intégré les graphiques et tableaux dans une page web hébergée sur GitHub.

---

# 7. La Création de la Page Web

Pour centraliser mes résultats, j’ai codé une **page HTML** hébergée sur GitHub. Cette page contient :

- Les graphiques interactifs (parkings vélos et voitures).
- Les graphiques en barres pour les écarts-types.
- La heatmap des corrélations.
- Des tableaux récapitulatifs et des explications des résultats.

J’ai pris soin de bien organiser cette page pour que les résultats soient accessibles et compréhensibles.

---

# 8. Conclusion

Ce projet m’a permis de développer des compétences en :

- **Collecte et traitement de données**
- **Analyse statistique et visualisation graphique**

J’ai étudié l’utilisation des parkings de Montpellier, analysé la relation entre l'occupation des parkings voitures et vélos, et créé des graphes et tableaux pour présenter mes résultats. J’ai également appris à résoudre des problèmes techniques liés aux graphiques interactifs et à intégrer mes analyses dans une page HTML accessible au maire de Montpellier et aux parties prenantes.

