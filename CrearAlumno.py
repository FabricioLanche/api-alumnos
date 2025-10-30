import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event.get('body', '{}'))
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    nombres = body.get('nombres')
    apellidos = body.get('apellidos')
    
    if not all([tenant_id, alumno_id, nombres, apellidos]):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id, alumno_id, nombres and apellidos are required'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.put_item(
        Item={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id,
            'nombres': nombres,
            'apellidos': apellidos
        }
    )
    # Salida (json)
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Alumno creado exitosamente', 'response': response}, default=str)
    }
