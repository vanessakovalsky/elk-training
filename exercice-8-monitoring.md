# Exercice 8 - Monitoring

## Utiliser Kibana pour monitorer son Elasticsearch

* Kibana propose des informations sur les metriques des index, aller voir dans Stack management ce que vous pouvez trouver
* Il est possible aussi avec Kibana de faire un tableau de bord pour monitorer son cluster elastic, notamment au niveaux des index, des noeuds et du cluster
* Vous pouvez par exemple vous inspirez de ce dashboard : https://elastic-content-share.eu/downloads/elastic-stack-monitoring-dashboard/ 

## Utiliser un outil externe pour monitorer, un exemple avec ElastiHQ

* Elastic HQ est un outil open source qui permet de monitorer avec une interface graphique son cluster Elasticsearch
* Pour l'installer : https://github.com/ElasticHQ/elasticsearch-HQ 
* Ou sous forme d'image Docker : https://hub.docker.com/r/elastichq/elasticsearch-hq/ 
* Rajoutons à notre fichier docker-compose un service avec cet image :
```
 elastichq:
    image: elastichq/elasticsearch-hq
    restart: always
    ports:
      - 5000:5000
    depends_on:
      - kibana
      - elasticsearch
```
* Une fois votre docker-compose relancer, vous aurez alors accès à l'interface sur localhost:5000 
* Explorer l'interface graphique pour découvrir les possibilités
* Si besoin, la documentation (en anglais) est ici : http://docs.elastichq.org/i 