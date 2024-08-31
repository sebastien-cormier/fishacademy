# fishacademy

La fishacademy est une partie mythique de Poker qui a lieu à Rouen 2 fois par mois.
Cette application a pour objectif de :

- Gérer la comptabilité (participation au repas, et puis c'est tout car les jeux d'argents sont interdits)
- Organiser les prochains évènements
- Suivre les caves/recaves durant la partie et avoir un classement final de la session
- Fournir des statistiques sur les résultats passés

Cette application répond aux besoins des parties FishAcademy, mais peut bien entendu être adaptée à tout type de partie privée.


## Pré-requis

Cetta application est développés en Pyhton et fourni une interface avec Streamlit. Elle se base sur des fichiers CSV et sur un stack elastic. Des fichiers de confs Docker sont fournis pour faciliter le développement en local. Le seul pré-requis indispensable étant donc d'avoir Docker Desktop installé sur son poste.


## Installation

Tout d'abord, 3 variables d'environnements doivent être paramétrées :

 - __ELASTIC_HOST__ : https://es01:9200
 - __ELASTIC_PASSWORD__ : ce que vous voulez
 - __ELASTIC_CERTIFICAT__ : /usr/share/kibana/config/certs/ca/ca.crt
 - __INIT_DATAS_DOC_ID__ : Id du google sheet servant de références aux datas

 Ces variables sont déclarées dans le fichier '_.env_EXAMPLE_' qu'il faut renommer en '_.env_EXAMPLE_' afin qu'il soit interpréter par docker compose. N'oubliez pas de modifier les valeurs '_CHANGE_ME_' présentent dans le fichier.
 
Pour lancer la stack elastic (elasticsearch, kibana) ainsi que Streamlit :

```
docker compose up -d
```

La stack elastic est lancé avec la sécurité activée. Le certificat nécessaire est monté dans un volume permettant à l'application fishacademy-app de se connecter au service.
Pour bien comprendre la configuration elastic avec docker compose, vous pouvez vous référer à l'article suivant : https://www.elastic.co/fr/blog/getting-started-with-the-elastic-stack-and-docker-compose

Le container avec l'application fishacademy-app monte un volume pour le code source, les resources ainsi que les données. Pour la bonne exécution de l'application, il est donc nécessaire d'initialiser l'index avec les bons settings/mappings et d'importer les données.

Pour l'import des données, le plus simple est de partir du fichier sur Google Sheet (n'hésitez pas à me demander l'accès) puis de faire un export CSV et la placer dans le répertoire _datas_. Ensuite, l'opération se fait de la façon suivante :

```
docker exec fishacademy-fishacademy-app-1 python reset_index_import_datas.py
```

Vous pouvez vérifier que tout est OK avec la commande suivante :

```
docker exec fishacademy-fishacademy-app-1 python check_elastic.py
```

Et en vous connectant sur _http://localhost:8501/_


## Principe de fonctionnement

Il n'y a qu'un seul index dans elasticsearch qui est à l'image du fichier présent sur Google Sheet. Ces données sont une liste de transaction qui peuvent être :

- Achat de jetons
- Revente de jetons (on rend les jetons à la fin. de la partie)
- Montant pour les cources
- Particiapations aux courses
- Transactions entre joueurs (dans ce cas, 2 lignes sont crées -> une pour créditer l'emetteur, l'autre pour débiter le bénéficiaire).

La gestion de la prochaine partie se fait tout simplement avec un fichier CSV sauvegardé dans _/datas_.

La gestion d'une partie se fait aussi via l'enregistrement des données dans un fichier CSV. L'indexation des données ne se fait qu'une fois la partie terminée et validée, c'est à dire quand l'argent sorti équivaut à l'argent rentré. 

 


