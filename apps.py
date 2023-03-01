import json
import numpy as np

def f(event, context):
    print("Ejecutando lambda con zappa")
    arr = np.array([1,2,3,4])
    print(arr)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


# zappa deploy dev
# test: zappa invoke apps.f

# actualizar:
# zappa update dev
# borrar: zappa undeploy