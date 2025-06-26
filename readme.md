# 🔌 Analyse Énergétique Territoriale – Temps Réel

Ce projet Streamlit permet de visualiser et d'analyser plusieurs indicateurs liés à l'énergie, à l’électricité, aux émissions de gaz à effet de serre (GES), ainsi qu'aux signaux de tension du réseau gazier (Ecogaz) à l’échelle nationale et régionale.

---

## 📊 Fonctionnalités principales

- **Données temps réel par région** : consommation et production d’électricité actualisées.
- **Carte interactive** des bornes de recharge pour véhicules électriques.
- **Analyse annuelle** de la production d’électricité par filière et par région.
- **Top 5 solaire** : classement des régions les plus productrices en énergie solaire.
- **Filière dominante** : carte par région de la source d’énergie prédominante.
- **Balance commerciale électricité** : imports, exports et solde net.
- **Signal Ecogaz** : suivi journalier de l’indice de tension sur le réseau gazier.
- **Émissions de GES** : bilan par opérateur et par scope (1 et 2).

---

## 🧾 Sources des données (Open Data Réseaux Énergies – ODRE)

- [Données temps réel électricité par région (eco2mix)](https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-tr/information/?disjunctive.nature&disjunctive.libelle_region)
- [Bornes de recharge IRVE (véhicules électriques)](https://odre.opendatasoft.com/explore/dataset/bornes-irve/information/?disjunctive.region&disjunctive.departement)
- [Production nationale annuelle par filière](https://odre.opendatasoft.com/explore/dataset/prod-national-annuel-filiere/information/)
- [Production régionale annuelle par filière](https://odre.opendatasoft.com/explore/dataset/prod-region-annuelle-filiere/information/?disjunctive.region)
- [Signal Ecogaz (indice de tension gazier)](https://odre.opendatasoft.com/explore/dataset/signal-ecogaz/information/)
- [Imports & exports commerciaux d’électricité](https://odre.opendatasoft.com/explore/dataset/imports-exports-commerciaux/information/)
- [Émissions de gaz à effet de serre par opérateur](https://odre.opendatasoft.com/explore/dataset/emissions-ges-operateurs/information/)
- [Données du signal Ecowatt](https://odre.opendatasoft.com/explore/dataset/nouveau_signal_ecowatt/information/)

---

## 📦 Technologies utilisées

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Folium](https://python-visualization.github.io/folium/)
- [Plotly](https://plotly.com/python/)
- [st_aggrid](https://github.com/PablocFonseca/streamlit-aggrid)

---

## ⚠️ Remarques

- Toutes les données proviennent de plateformes publiques et sont mises à jour automatiquement via les API ODRE.
- Les données temps réel peuvent varier légèrement selon les latences de publication.

---

## 📄 Licence

Ce projet est proposé à des fins éducatives. Les données utilisées sont libres d’accès via le portail ODRE.