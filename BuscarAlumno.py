import json
import boto3

def lambda_handler(event, context):
    # Si el evento viene desde API Gateway, parsea el body
    if 'body' in event:
        try:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        except json.JSONDecodeError:
            body = {}
    else:
        # Si se ejecuta directamente desde la consola Lambda
        body = event

    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response, ensure_ascii=False)
    }
