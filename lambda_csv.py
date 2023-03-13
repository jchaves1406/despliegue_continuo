from web_sc_functions import leer_pagina, obtener_bloques_informacion,\
    extraer_atributos_casa, crear_dataframe_casas
import json
import boto3
import datetime
import io

s3 = boto3.client('s3')


def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'landing-casas-xxx'
    key = '2023-03-13.html'
    file_name_html = datetime.datetime.utcnow().strftime('%Y-%m-%d') + '.html'
    print(key)
    print(file_name_html)

    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response['Body'].read()

    # Se genera contenido en html para obtener el parse.html
    page = leer_pagina(content)

    # Se utilizan las funciones para el webscraping
    bloques = obtener_bloques_informacion(page)
    atributos_casas = extraer_atributos_casa(bloques)
    df_casas = crear_dataframe_casas(atributos_casas)

    # Se genera dataframe con el resultado de las consultas
    print(df_casas)

    # Se guarda csv en otro bucket final
    file_name_csv = datetime.datetime.utcnow().strftime('%Y-%m-%d') + '.csv'
    bucket_name = 'casas-final-xxx'
    df_casas.to_csv(file_name_csv, index=False)

    # Genera el archivo CSV en memoria
    csv_buffer = io.StringIO()
    df_casas.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Sube el archivo a S3
    s3.put_object(Bucket=bucket_name, Key=file_name_csv,
                  Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps(" guardado.")
    }
