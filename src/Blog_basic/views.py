from django.shortcuts import render
from datetime import datetime
import socket
import requests

API_ADDRESS = "http://ip-api.com/json/"

#VUE
def index(request):
        date = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        hostname = socket.gethostname()
        ip_locale = socket.gethostbyname(hostname)
        return render(request,"index.html",
                      context={"prenom":"Fabrice",
                               "date":date,
                               "hostname":hostname,
                               "ip_locale":ip_locale,
                               "ip_info":get_ip_info(),
                               "client_ip":get_client_ip(request)})

def get_ip_info():
    try:
        response = requests.get(API_ADDRESS, timeout=5)
        response.raise_for_status()
        return response.json()
    except:
        return {"error": "Erreur connexion"}

#fonction pour récupérer l'adresse du client
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()  # première IP de la liste
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip