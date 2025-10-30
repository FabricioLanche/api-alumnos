import boto3  # import Boto3
import json  # import json

def lambda_handler(event, context):
    # Entrada (json)
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
    
    tenant_id = body.get('tenant_id')
    
    if not tenant_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id is required'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.query(
        KeyConditionExpression='tenant_id = :tenant_id',
        ExpressionAttributeValues={
            ':tenant_id': tenant_id
        }
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'body': json.dumps(response, default=str)
    }
