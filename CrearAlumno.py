import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body)
    
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    alumno_datos = body.get('alumno_datos')
    
    if not all([tenant_id, alumno_id, alumno_datos]):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id, alumno_id and alumno_datos are required'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.put_item(
        Item={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id,
            'alumno_datos': alumno_datos
        }
    )
    # Salida (json)
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Alumno creado exitosamente', 'response': response}, default=str)
    }
