# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests

# URL base de la API ESIOS
base_url = "https://api.esios.ree.es/indicators?locale=en"

# Configurar los headers
headers = {
    "Accept": "application/json; application/vnd.esios-api-v1+json",
    "Content-Type": "application/json",
    "x-api-key": "99e6f035c49454f9a148b53a32ff296e3012db82d2c8645d13b0ed7ff3e77aba"
}


def get_indicators():
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(data)
        # Imprimimos todos los indicadores disponibles en inglés
        # y busco los que tengan Margin en el nombre y los Intradays 1 al 7 para sacar sus ids
        for indicator in data["indicators"]:
            print(f"ID: {indicator['id']} - Name: {indicator['name']}")
    else:
        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    get_indicators()
