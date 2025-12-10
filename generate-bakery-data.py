import json
from datetime import datetime, timedelta
import random

# Configuration
PRODUITS = {
    "Croissant": {"categorie": "Viennoiserie", "prix": 1.20},
    "Pain au chocolat": {"categorie": "Viennoiserie", "prix": 1.30},
    "Baguette": {"categorie": "Pain", "prix": 1.10},
    "Pain complet": {"categorie": "Pain", "prix": 1.80},
    "Pain de mie": {"categorie": "Pain", "prix": 2.50},
    "Éclair au chocolat": {"categorie": "Pâtisserie", "prix": 3.50},
    "Tarte aux pommes": {"categorie": "Pâtisserie", "prix": 4.20},
    "Millefeuille": {"categorie": "Pâtisserie", "prix": 4.50},
    "Macaron": {"categorie": "Pâtisserie", "prix": 2.00},
    "Sandwich jambon": {"categorie": "Snacking", "prix": 4.50},
    "Sandwich poulet": {"categorie": "Snacking", "prix": 5.00},
    "Quiche lorraine": {"categorie": "Snacking", "prix": 3.80},
    "Cookie": {"categorie": "Biscuiterie", "prix": 1.50},
    "Brownie": {"categorie": "Biscuiterie", "prix": 2.50}
}

VENDEURS = ["Marie", "Pierre", "Sophie", "Jean"]
MODES_PAIEMENT = ["CB", "Espèces", "Sans contact"]

# Générer 7 jours de données (une semaine complète)
start_date = datetime.now() - timedelta(days=7)

documents = []

for day in range(7):
    current_date = start_date + timedelta(days=day)
    
    # Heures d'ouverture : 7h - 20h
    for hour in range(7, 20):
        # Plus de ventes entre 8h-9h (petit-déj), 12h-14h (déjeuner), 16h-18h (goûter)
        if hour in [8, 9]:
            nb_ventes = random.randint(15, 25)
        elif hour in [12, 13]:
            nb_ventes = random.randint(20, 30)
        elif hour in [16, 17, 18]:
            nb_ventes = random.randint(10, 20)
        else:
            nb_ventes = random.randint(5, 12)
        
        for _ in range(nb_ventes):
            # Timestamp aléatoire dans l'heure
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            timestamp = current_date.replace(hour=hour, minute=minute, second=second)
            
            # Choisir un produit (avec pondération)
            if hour in [7, 8, 9]:  # Matin : viennoiseries
                produits_possibles = [p for p in PRODUITS.keys() 
                                     if PRODUITS[p]["categorie"] == "Viennoiserie"]
            elif hour in [12, 13, 14]:  # Midi : snacking
                produits_possibles = [p for p in PRODUITS.keys() 
                                     if PRODUITS[p]["categorie"] in ["Snacking", "Pain"]]
            elif hour in [16, 17, 18]:  # Goûter : pâtisseries
                produits_possibles = [p for p in PRODUITS.keys() 
                                     if PRODUITS[p]["categorie"] in ["Pâtisserie", "Biscuiterie"]]
            else:
                produits_possibles = list(PRODUITS.keys())
            
            produit = random.choice(produits_possibles)
            quantite = random.randint(1, 4)  # 1 à 4 unités
            prix_unitaire = PRODUITS[produit]["prix"]
            total = round(quantite * prix_unitaire, 2)
            
            doc = {
                "timestamp": timestamp.isoformat(),
                "produit": produit,
                "categorie": PRODUITS[produit]["categorie"],
                "quantite": quantite,
                "prix_unitaire": prix_unitaire,
                "total": total,
                "vendeur": random.choice(VENDEURS),
                "mode_paiement": random.choice(MODES_PAIEMENT)
            }
            
            documents.append(doc)

# Générer le fichier bulk pour ElasticSearch
with open("bakery_bulk.json", "w", encoding="utf-8") as f:
    for i, doc in enumerate(documents):
        # Ligne d'index
        f.write(json.dumps({"index": {"_id": str(i+1)}}) + "\n")
        # Document
        f.write(json.dumps(doc) + "\n")

print(f"Généré {len(documents)} ventes")
print(f"Fichier bakery_bulk.json créé")
print(f"Période : {start_date.date()} à {(start_date + timedelta(days=7)).date()}")

# Statistiques
total_ca = sum(doc["total"] for doc in documents)
print(f"CA total : {total_ca:.2f}€")
