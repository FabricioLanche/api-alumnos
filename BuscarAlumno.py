import boto3

def lambda_handler(event, context):
    # Entrada (json)
    query_params = event.get('queryStringParameters', {})
    tenant_id = query_params.get('tenant_id')
    alumno_id = query_params.get('alumno_id')
    
    # Validación básica
    if not tenant_id or not alumno_id:
        return {
            'statusCode': 400,
            'body': 'tenant_id and alumno_id are required'
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'response': response
    }
