import requests


def display_table(data):
    pass


# URL de la requête
url = "http://localhost:8080/api/v2/auth/login"

# En-têtes de la requête
headers = {
    'Referer': 'http://localhost:8080'
}

# Données de la requête
data = {
    'username': 'admin',
    'password': 'adminadmin'
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, data=data)

# Affichage de la réponse
print(response.status_code)  # Statut de la réponse
print(response.headers)  # En-têtes de la réponse
print(response.text)  # Corps de la réponse

cookie = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
print(cookie)

url = "http://localhost:8080/api/v2/torrents/info?&sort=ratio"

# Cookies de la requête
cookies = {
    'SID': cookie
}

# Envoi de la requête GET
response = requests.get(url, cookies=cookies)

# Affichage de la réponse
print(response.status_code)  # Statut de la réponse
print(response.headers)  # En-têtes de la réponse
print(response.text)  # Corps de la réponse
