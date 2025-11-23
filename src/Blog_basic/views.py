from django.shortcuts import render
from datetime import datetime
import socket
import requests
import folium

API_ADDRESS = "http://ip-api.com/json/"

#VUE
def index(request):
        date = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        hostname = socket.gethostname()
        ip_local = socket.gethostbyname(hostname)
        ip_info = get_ip_info()

        map_html = generate_map(ip_info)

        return render(request,"index.html",
                      context={"prenom":"Fab",
                               "date":date,
                               "hostname":hostname,
                               "ip_local":ip_local,
                               "ip_info":get_ip_info(),
                               "client_ip":get_client_ip(request),
                               "map_html": map_html})

def get_ip_info():
    try:
        response = requests.get(API_ADDRESS, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get('status') == 'success':
            return data
        else:
            return {"error": "API a retourné une erreur"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur connexion: {str(e)}"}


def generate_map(ip_info):
    """Génère la carte HTML avec Folium"""
    # Vérifier si on a les coordonnées
    if ip_info.get('lat') and ip_info.get('lon'):
        try:
            lat = float(ip_info['lat'])
            lon = float(ip_info['lon'])

            # Créer la carte centrée sur les coordonnées
            m = folium.Map(
                location=[lat, lon],
                zoom_start=13,
                width='100%',
                height='100%',
                tiles='OpenStreetMap'
            )

            # Ajouter un marqueur avec popup
            popup_text = f"""
            <b>{ip_info.get('city', 'Ville inconnue')}</b><br>
            {ip_info.get('country', 'Pays inconnu')}<br>
            IP: {ip_info.get('query', 'N/A')}
            """

            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_text, max_width=250),
                tooltip="📍 Votre localisation",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

            # Ajouter un cercle autour du point
            folium.Circle(
                [lat, lon],
                radius=500,  # 500 mètres
                color='#4a7c9e',
                fill=True,
                fillColor='#4a7c9e',
                fillOpacity=0.2
            ).add_to(m)

            # Convertir en HTML
            return m._repr_html_()
        except Exception as e:
            return f'<div style="color: #c75450; padding: 2rem;">Erreur lors de la génération de la carte: {str(e)}</div>'
    else:
        return '<div style="color: #a0a0a0; padding: 2rem;">Coordonnées GPS non disponibles</div>'



#fonction pour récupérer l'adresse du client
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()  # première IP de la liste
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip