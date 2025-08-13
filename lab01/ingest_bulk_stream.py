import json
import random
import string
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from elasticsearch import Elasticsearch, helpers
import json
import os
from datetime import datetime, timedelta

# =======================
# CONFIGURATION
# =======================
ELASTIC_URL = "http://104-200-27-215.ip.linodeusercontent.com:9200/"  # Elasticsearch endpoint
INDEX_NAME = "transactions"              # Nom de l'index
USERNAME = "elastic"                    # Utilisateur (si auth)
PASSWORD = "vUVv0t19ZWW14QqAzl36270P"                   # Mot de passe (si auth)

NUM_THREADS = 8                         # Nombre de flux concurrents
BATCH_SIZE = 500                        # Nombre de documents par envoi
DELAY_BETWEEN_BATCHES = 0.1             # Délai entre chaque envoi (en secondes)

RUN_PER_BATCH = False

client = Elasticsearch(
    ELASTIC_URL,
    verify_certs=False,
    basic_auth=(USERNAME, PASSWORD)
)
# =======================
# FONCTIONS
# =======================

def random_string(length=10):
    """Génère une chaîne aléatoire."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_bulk_payload(batch_size):
    """Crée un payload Bulk pour Elasticsearch."""
    bulk_data = []
    for _ in range(batch_size):

        start_at = datetime.now() - timedelta(days=random.randrange(1, 2500))
        validity = random.randint(1, 720)
        end_at = start_at + timedelta(days=validity)
        action = {"index": {}}
        document = {
            "num_clients": "07" + str("".join(random.choices('0123456789', k=8))),
            "offre": "mix_mois_1",
            "montant": random.randint(100, 20000),
            "avantages": f"100GO et 60min valable {validity} jours",
            "date_achat": start_at.isoformat(),
            "date_fin_validite": end_at.isoformat(),
            "validite": validity,

            "_op_type": "create",
            "@timestamp": datetime.now().isoformat(),
        }

        #bulk_data.append(json.dumps(action))
        #bulk_data.append(json.dumps(document))
        bulk_data.append(document)

        if _ == 0:
          print(document)

    return bulk_data

def send_bulk():
    """Envoie un batch de données à Elasticsearch."""
    payload = generate_bulk_payload(BATCH_SIZE)
    try:
        helpers.bulk(
            client,
            payload,
            index=INDEX_NAME
        )
        time.sleep(DELAY_BETWEEN_BATCHES)
    except Exception as e:
        print(f"Erreur d'envoi : {e}")
        time.sleep(1)  # Pause avant de réessayer
        raise e

def send_bulk_many():
    while True:
        send_bulk()
# =======================
# LANCEMENT
# =======================
if __name__ == "__main__":
    if not RUN_PER_BATCH:
        print(f"🚀 Lancement de 01 bulk de  {BATCH_SIZE} données...")
        start_at = time.perf_counter()
        send_bulk()
        end_at = time.perf_counter()

        print(f"Temps d'envoi : {end_at - start_at:.2f} secondes")
        exit()
