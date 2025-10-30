import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    body = json.loads(event.get('body', '{}'))
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
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Alumno eliminado exitosamente', 'response': response}, default=str)
    }
