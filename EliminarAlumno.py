import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body)
    
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    
    if not all([tenant_id, alumno_id]):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id and alumno_id are required'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    # Primero verificar si existe
    get_response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    
    if 'Item' not in get_response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Alumno no encontrado'})
        }
    
    # Eliminar
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        ReturnValues='ALL_OLD'
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Alumno eliminado exitosamente',
            'alumno_eliminado': response.get('Attributes')
        }, default=str)
    }
