# données sur les jeux olympiques et paralympiques de Paris 2024

- scraping du [site officiel olympics.com](https://olympics.com/) car les données ne sont pas disponibles en open data. La plupart des contenus est aussi planquée derrière le front react ce qui empêche de les récupérer proprement. Le code de production des donnés sont dans le répertoire `./recipes`.
- les données sur les résultats sont récupérées automatiquement [toutes les 10 minutes](https://github.com/taniki/paris2024-data/actions).
- 🙏 si vous utilisez ces données dans le cadre d'une publication, il serait très appréciable de me mentionner et faire un lien vers ce dépôt.
  - Par exemple : `source : Paris 2024, traitement des données : tam kien duong`


## les données automatisées

- `datasets/medals.csv` : liste de toutes les médailles avec les informations sur l'athlète, la discipline et l'événement
- `datasets/medallists.csv` : liste des médaillé·es avec le nombre de médailles et le code du pays
- `datasets/medal_countries.wide.auto.csv` : liste des pays avec le nombre de médailles
- `datasets/medal_countries.long.auto.csv` : la même chose mais au format `long`, une ligne par combinaison de pays et couleur de médaille.
