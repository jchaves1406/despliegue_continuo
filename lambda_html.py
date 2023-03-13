import boto3
import datetime
from web_sc_functions import descargar_pagina


s3 = boto3.client('s3')


def lambda_handler():
    url = '''https://casas.mitula.com.co/searchRE/orden-0/op-1/q-chapinero-
             bogota/pag-1?req_sgmt=REVTS1RPUDtVU0VSX1NFQVJDSDtTRVJQOw=='''

    # Se descarga el contenido de la url con la función implementada
    content = descargar_pagina(url)

    # Se guarda el contenido de la pagina en un archivo html en el bucket
    bucket_name = 'landing-casas-xxx'
    file_name = datetime.datetime.utcnow().strftime('%Y-%m-%d') + '.html'
    s3.put_object(Bucket=bucket_name, Key=file_name,
                  Body=content, ContentType='text/html')

    return {
        'statusCode': 200,
        'body': 'El archivo ' + file_name + ' se guardo con exito'
    }


lambda_handler()
