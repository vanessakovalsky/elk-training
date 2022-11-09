# Exercice 10 - Snapshot et restauration


## Créer des snapshots

* Pour commencer, nous avons besoin de déclarer un dépôt de snapshot, dans lequel ceux-ci seront enregistrés. 
* Il est possible de choisir parmi les différents types de dépôts existants lequel utilisé pour stocker ses snapshots : https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html 
* Ici, nous avons choisi S3, il est nécessaire d'installer le plugin correspondant sur elasticsearch :
```
sudo bin/elasticsearch-plugin install repository-s3
```
* Puis de définir le dépôt
```
PUT _snapshot/backups
{
    "type": "s3",
    "settings": {
      "bucket": "elastic",
      "endpoint": "10.3.10.10:9000",
      "protocol": "http"
    }
}
```
* Nous ajoutons également les éléments de connexions, en nous connectant sur le conteneur docker d'elasticsearch :
```
bin/elasticsearch-keystore add s3.client.default.access_key
bin/elasticsearch-keystore add s3.client.default.secret_key
```
* Puis nous pouvons créer notre snapshot
```
PUT /_snapshot/backup/my_snapshot-01-10-2019
```
* Il est aussi possible de spécifier les index à mettre dans le snapshot avec l'option indices de la requête :
```
PUT /_snapshot/backup/my_snapshot-01-10-2019
{
  "indices": "my_index_1,my_index_2"
  }
}
```

* Il est possible d'automatiser ses snapshots avec l'utilisataire curator-cli : https://www.elastic.co/guide/en/elasticsearch/client/curator/current/command-line.html 

## Présentation du contenu d'un snapshot

* Les fichiers créés lors d'un snapshot sont les suivants :
    * index-N — Liste de tous les IDs de Snapshot et des indexes qu'ils contiennent. N est le numéro de génération du fichier. Ce fichier fait correspondre les snapshots aux index.
    index.latest — Contient un nombre de dernier fichier Index-N (utilisé dans les depôts qui n'autorisent pas les listes).
    * incompatible-snapshots — Liste des snapshots qui ne sont plus compatible avec cette version de cluster.
    * snap-YYYYMMDD.dat — Métadonnées des Snapshot pour ce snapshot (pas toujours avec le le format de date dans le nom) 
    * meta-YYYYMMDD.dat — Métadonnées globales si elles sont inclues dans ce snapshot (pas toujours avec le le format de date dans le nom)
    * indices/ — Dossier avec tous les données d'index, par shard
    * 0McTFz3XRFSSMUIotGKKog — Dossier d'index assigné au dépôt, un par Index
    * meta-YYYYMMDD.dat — Métadonnées pour cet index, pour un snapshot particulier
    * 0/ — Dossier pour le 0 — il peut contenir des milliers de sous-dossier de segments
    * snap-YYMMDD.dat — Fait correspondre les fichiers de segment aux noms dans le dépôt
    * __VPO5oDMVT5y4Akv8T_AO_A — Fichiers de segments, voir snap-* pour faire correspondre les fichiers de segments

## Restauration

* Commençons par lister les snapshots
```
GET _snapshot
```
* Une fois le snaphshot choisi, nous commençons par supprimer l'index
```
# Delete an index
DELETE my-index
```
* Puis nous pouvons restaurer notre snapshot
```
POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
{
  "indices": "my-index,logs-my_app-default"
}
```
* Pour suivre votre restauration
```
GET _cluster/health
GET my-index/_recovery
```



