from bs4 import BeautifulSoup
from web_sc_functions import extraer_atributos_casa, \
    obtener_bloques_informacion
from unittest import mock


@mock.patch('web_sc_functions.descargar_pagina')
def test_descargar_pagina(mock_descargar_pagina):
    url = "https://www.google.com"
    page = mock_descargar_pagina(url)
    mock_descargar_pagina.assert_called_once_with(url)
    assert page is not None


def test_obtener_bloques_informacion():
    # HTML de ejemplo
    html = '''<div class="listing-card__information">Bloque 1</div>
            <div class="listing-card__information">Bloque 2</div>'''
    soup = BeautifulSoup(html, 'html.parser')

    # Obtener los bloques de información con la función
    bloques = obtener_bloques_informacion(soup)

    # Verificar que se obtuvieron los bloques correctos
    assert len(bloques) == 2
    assert bloques[0].text == "Bloque 1"
    assert bloques[1].text == "Bloque 2"


def test_extraer_atributos_casa():
    bloque1 = BeautifulSoup(
        '''<div class="listing-card__content">
        <div class="listing-card__properties">
            <span class="listing-card__property-icon icon-rooms"></span>
            <span>3</span><span class="listing-card__property-icon icon-bath">
    </span><span>2</span></div><div class="listing-card__title">Barrio1</div>
            <div class="price">$100</div></div>''', 'html.parser')
    bloque2 = BeautifulSoup(
        '''<div class="listing-card__content">
            <div class="listing-card__properties">
                <span class="listing-card__property-icon icon-rooms">
    </span><span>4</span><span class="listing-card__property-icon icon-bath">
    </span><span>3</span></div><div class="listing-card__title">Barrio2</div>
                <div class="price">$200</div></div>''', 'html.parser')
    bloques = [bloque1, bloque2]

    resultado = extraer_atributos_casa(bloques)

    assert resultado[0]['barrio'] == 'Barrio1'
    assert resultado[0]['precio'] == '$100'
    assert resultado[1]['barrio'] == 'Barrio2'
    assert resultado[1]['precio'] == '$200'
