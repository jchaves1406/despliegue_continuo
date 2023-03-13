from bs4 import BeautifulSoup
import pandas as pd
import datetime
import requests


def descargar_pagina(url):
    page_content = requests.get(url).text

    return page_content


def leer_pagina(url):
    page = BeautifulSoup(url, "html.parser")
    return page


def obtener_bloques_informacion(page):
    bloques = page.find_all(
        "div", attrs={"class": "listing-card__information"})
    return bloques


def extraer_atributos_casa(bloques):
    # Definir un diccionario con las claves de los atributos a obtener
    plantilla = {"barrio": None, "precio": None,
                 "habitaciones": None, "baños": None, "m²": None}
    casas = []
    # Iterar sobre cada bloque y obtener la información relevante
    for bloque in bloques:
        propiedades = bloque.find_all(
            'div', {'class': 'listing-card__properties'})
        atributos = [span.text.strip()
                     for propiedad in propiedades
                     for span in propiedad.find_all('span')]
        casa_dict = {clave: "N/A" for clave in plantilla}
        for att in atributos:
            for clave in casa_dict:
                if clave in att:
                    casa_dict[clave] = att
                    break
        casa_dict['barrio'] = bloque.find(
            "div", attrs={"class": "listing-card__title"}).text
        casa_dict['precio'] = bloque.find("div", attrs={"class": "price"}).text

        casas.append(casa_dict)
    return casas


def crear_dataframe_casas(atributos_casas):
    df = pd.DataFrame(atributos_casas)

    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    df.insert(0, 'FechaDescarga', fecha_actual)

    # Renombrar columnas
    nombres_columnas = {
        "FechaDescarga": "Fecha Descarga",
        "barrio": "Barrio",
        "precio": "Valor",
        "habitaciones": "NumHabitaciones",
        "baños": "NumBanos",
        "m²": "mts2"
    }

    df = df.rename(columns=nombres_columnas)
    return df
