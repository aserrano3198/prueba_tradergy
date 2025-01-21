import requests
import pandas as pd


def download_esios_data(start_date, end_date):
    # Indicadores para Day Ahead y sesiones intradiarias sacados de get_indicators.py
    indicators = {
        "Day Ahead": 600,
        "Intraday 1": 612,
        "Intraday 2": 613,
        "Intraday 3": 614,
        "Intraday 4": 615,
        "Intraday 5": 616,
        "Intraday 6": 617,
        "Intraday 7": 618,
    }

    all_data = []
    url_template = "https://api.esios.ree.es/indicators/{indicator}"
    headers = {
        "Accept": "application/json; application/vnd.esios-api-v1+json",
        "Content-Type": "application/json",
        "x-api-key": "99e6f035c49454f9a148b53a32ff296e3012db82d2c8645d13b0ed7ff3e77aba"
    }

    for session_name, indicator in indicators.items():
        print(f"Downloading data from {session_name}...")
        url = url_template.format(indicator=indicator)
        params = {"start_date": start_date, "end_date": end_date, "time_trunc": "hour"}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()["indicator"]["values"]
            df = pd.DataFrame(data)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df["value"] = df["value"].astype(float)
            df = df[df["geo_name"] == "España"]
            df = df[["datetime", "value"]]
            df["session"] = session_name
            all_data.append(df)
        else:
            print(f"Error {response.status_code} al obtener {session_name}: {response.text}")

    # Combinar todos los datos en un único DataFrame
    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.sort_values(by=["datetime", "session"]).reset_index(drop=True)
    return final_df

if __name__ == '__main__':
    df = download_esios_data("2024-01-01T00:00:00", "2024-12-31T23:59:59")
    df.to_csv("precios_spot.csv", index=False)
