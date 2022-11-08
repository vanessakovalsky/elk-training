# Exercice 9 - Répartition de charge

## Réplication entre noeuds

### Définir les différents noeuds et leur attributs

* Nous allons définir que les node 1 et 3 de notre cluster seront des nodes avec l'attribut 'hot', et le node 2 sera un node avec l'attribut 'cold'  
* Pour cela dans chaque fichier de configuration elasticsearch.yml de chaque noeud, ajouter la ligne : `node.attr.temp: hot` pour les node 1 et 3 et la ligne `node.attr.temp: cold` pour le node 2
* Redémarrer votre cluster pour que cet attribut soit pris en compte
* Puis ajoutons pour notre index heroes l'allocation sur les nodes avec l'attribut 'hot' :
```
PUT heroes/_settings
{
  "index.routing.allocation.require.temp": "hot"
}
```
* Puis notre index villains sur le noeud avec l'attribut cold :
```
PUT villains/_settings
{
  "index.routing.allocation.require.temp": "cold"
}
```
* Si vous vérifiez ou sont vos index, ceux ci devraient être positionner maintenant sur les bons noeuds

### Gestion des shards et des replicas

* Pour calculer le nombre de shards nécessaire vous pouvez utiliser la formule de calcul suivante :
    * de 0 à 3 millions de documents : 1 shard
    * de 3 à 5 millions de documents : 2 shard
    * au delà : (nombrededocument / 5 millions) + 1 shards
* Pour l'exemple et la manipulation (ce n'est pas nécessaire dans le cas présent), nous allons augmenter à 3 le nombre de shard de notre index heroes
* On peut le faire avec l'API Split par exemple (le nombre de shard doit alors être un multiple du nombre de shard original), pour commencer, on met l'index en lecture seule
```
PUT heroes/_settings
{
  "index.blocks.write": true
}
```
* Puis on définit le nombre de shard pour le split :
```
POST /heroes/_split/test_split_target
{
  "settings": {
    "index.number_of_shards": 3
  }
}
```
* Enfin on remet l'index en écriture
```
PUT heroes/_settings
{
    "index.blocks.write": null
}
```
* Vérifier les shards créés

## Réplication inter-cluster

### Ajout d'un autre cluster

* Dupliquer votre dossier contenant le docker-compose.yaml et sa configuration
* Dans le dossier dupliqué, modifier les ports utilisés sur votre hôte ainsi que les noms de services
* Lancer votre deuxième cluster
* Celui-ci va nous permettre de créer de la réplication


### Réplication des données

* A l'aide de Kibana, ou de la requête suivante, sur votre premier cluster, nous allons déclarer le deuxième cluster au premier :
```
# À partir de "cluster1", nous définirons comment accéder à "cluster2"
PUT /_cluster/settings
{
  "persistent" : {
    "cluster" : {
      "remote" : {
        "cluster2" : {
          "seeds" : [
            "127.0.0.1:9300"
          ]
        }
      }
    }
  }
}
```
* Maintenant que nos deux clusters savent communiquer, nous allons créer un index à répliquer
```
# Créer un index "product"
PUT /products
{
  "settings" : {
    "index" : {
      "number_of_shards" : 1,
      "number_of_replicas" : 0,
      "soft_deletes" : {
        "enabled" : true      
      }
    }
  },
  "mappings" : {
    "_doc" : {
      "properties" : {
        "name" : {
          "type" : "keyword"
        }
      }
    }
  }
}
```
* Puis nous lançons la réplication depuis notre cluster1
```
PUT /products-copy/_ccr/follow
{
  "remote_cluster" : "cluster2",
  "leader_index" : "products"
}
```
* Pour tester nous ajoutons un document sur le cluster1
```
POST /products/_doc
{
  "name" : "My cool new product"
}
```
* Puis nous vérifions sur le deuxième cluster
```
GET /products-copy/_search
```
* Notre réplication doit maintenant être en place

### Quelques commandes utiles 

```
# Retourner toutes les statistiques associées à la CCR
GET /_ccr/stats
# Mettre en pause la réplication d'un index donné
POST /<follower_index>/_ccr/pause_follow
# Reprendre la réplication, dans la plupart des cas après sa mise en pause
POST /<follower_index>/_ccr/resume_follow
{
}
# Ne plus suivre un index (arrêter la réplication pour l'index de destination), ce qui nécessite d'abord de mettre en pause la réplication 
POST /<follower_index>/_ccr/unfollow
# Statistiques pour un index suiveur
GET /<index>/_ccr/stats
# Supprimer un modèle de suivi automatique
DELETE /_ccr/auto_follow/<auto_follow_pattern_name>
# Afficher tous les modèles de suivi automatique, ou obtenir un modèle de suivi automatique par nom
GET /_ccr/auto_follow/
GET /_ccr/auto_follow/<auto_follow_pattern_name>
```

