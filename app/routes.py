from flask import Blueprint, render_template, current_app
import requests
import matplotlib.pyplot as plt
import io
import base64
import os

main = Blueprint('main', __name__)

QB_URL = os.getenv('QB_URL', 'http://qbittorrent:8080')
QB_USERNAME = os.getenv('QB_USERNAME', 'ton_username')
QB_PASSWORD = os.getenv('QB_PASSWORD', 'ton_password')


def convert_size_humanreadable(taille_en_bytes: int) -> str:
    taille_en_gib = taille_en_bytes / (1024 ** 3)
    taille_en_mib = taille_en_bytes / (1024 ** 2)

    if taille_en_gib >= 1:
        return f"{taille_en_gib:.2f} Gib"
    else:
        return f"{taille_en_mib:.2f} Mib"


@main.route('/')
def index():
    try:
        session = requests.Session()
        # Ajout de l'en-tête Referer pour l'authentification
        headers = {'Referer': QB_URL}
        auth_response = session.post(f'{QB_URL}/api/v2/auth/login',
                                     headers=headers,
                                     data={'username': QB_USERNAME, 'password': QB_PASSWORD})

        if auth_response.status_code == 403:
            current_app.logger.error("IP de l'utilisateur bannie pour trop de tentatives de connexion échouées")
            return "Accès refusé", 403
        elif auth_response.status_code != 200:
            current_app.logger.error(
                f"Échec de l'authentification : {auth_response.status_code} - {auth_response.text}")
            return "Échec de l'authentification", 500

        # Utilisation du cookie SID pour les requêtes nécessitant une authentification
        sid_cookie = auth_response.cookies.get('SID')
        if not sid_cookie:
            current_app.logger.error("Échec de récupération du cookie SID")
            current_app.logger.debug(dict(auth_response.cookies))
            return "Échec de récupération du cookie SID", 500

        cookies = {'SID': sid_cookie}
        response = session.get(f'{QB_URL}/api/v2/torrents/info', cookies=cookies)

        if response.status_code != 200:
            current_app.logger.error(f"Erreur de récupération des torrents : {response.status_code} - {response.text}")
            return "Erreur de récupération des torrents", 500

        # Conversion des valeurs avant de les passer au template
        torrents = [{
            'name': torrent['name'],
            # Convertir la taille de bytes en Go (1 Go = 2^30 bytes)
            'size': convert_size_humanreadable(torrent['size']),
            # Convertir le temps actif de secondes en jours (1 jour = 86400 secondes)
            'time_active': f"{torrent['time_active'] / 86400:.2f} jours",
            # Convertir uploadé de bytes en Go
            'uploaded': convert_size_humanreadable(torrent['uploaded']),
            # Calcule du score torrent
            'score_torrent': f"{(torrent['uploaded'] / torrent['size']) / (torrent['time_active'] / 86400) if torrent['time_active'] > 0 else 0:.4f}"
        } for torrent in response.json()]
        return render_template('index.html', torrents=torrents)

    except Exception as e:
        current_app.logger.error(f"Exception : {e}")
        return "Erreur interne du serveur", 500
