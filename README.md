# SAE15_Audrey_Authier-Cassagne

# Genèse de Mon Projet

Dans le cadre de ma formation en **BUT Réseaux et Télécommunications**, j'ai été mandatée par la mairie de Montpellier pour réaliser une étude sur l’utilisation des parkings de la ville, dans le cadre de la **SAE 15**. Cette étude avait pour but de répondre à plusieurs questions concernant les parkings voitures et vélos, en particulier sur leur taux d'occupation et la relation entre l’utilisation des parkings de véhicules et de vélos. Le projet visait également à analyser si ces parkings étaient bien dimensionnés, et à observer les corrélations potentielles entre les parkings pour mieux comprendre leur utilisation.

## 1. Mise en Situation et Objectifs du Projet

Le maire de Montpellier m’a mandaté pour étudier l’occupation des parkings de la ville, en particulier :

- Le taux d’occupation des parkings voitures et vélos.
- L’analyse de la relation entre l’utilisation des parkings de voitures et de vélos, pour voir s’il existait des liens entre l’utilisation des parkings voitures et des parkings vélos situés à proximité.

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

## 4. Traitement des Données

Après avoir récupéré les données nécessaires, j’ai procédé à leur traitement pour calculer les **taux d’occupation des parkings**. Cependant, en raison de la différence de nature des parkings (voitures et vélos), les calculs ont été adaptés :

### Taux d'occupation des parkings voitures :
Le **taux d’occupation des parkings voitures (en %)** est calculé comme suit :

```math
\text{taux d'occupation voitures} = \left( 1 - \frac{\text{places libres}}{\text{capacité totale}} \right) \times 100
