import requests, json
from zilonis.constantes import constantes

def getEmision(token, **data):
    url = constantes.API+'/api/v1/emision'
    headers = {'Accept':'application/json','Authorization':'Bearer '+token}

    response = requests.post(url, json=data, headers=headers, timeout=30)

    if response.status_code == 200:
        response_json = json.loads(response.text)
    elif response.status_code == 401:
        response_json = {'Error':'Acceso Denegado'}
    else:
        response_json = {'Error':'Servicio fuera linea'}

    return response_json

def getPoliza(token, **data):
    url = constantes.API+'/api/v1/emision/imprime/poliza'
    headers = {'Accept':'application/json','Authorization':'Bearer '+token}

    response = requests.post(url, json=data, headers=headers, timeout=20)

    if response.status_code == 200:
        response_json = json.loads(response.text)
    elif response.status_code == 401:
        response_json = {'Error':'Acceso Denegado'}
    else:
        response_json = {'Error':'Servicio fuera linea'}

    return response_json
