import boto3
import json

def lambda_handler(event, context):
    # Entrada (json)
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body)
    
    tenant_id = body.get('tenant_id')
    alumno_id = body.get('alumno_id')
    nombres = body.get('nombres')
    apellidos = body.get('apellidos')
    
    if not all([tenant_id, alumno_id]):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'tenant_id and alumno_id are required'})
        }
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    update_expression = []
    expression_values = {}
    
    if nombres:
        update_expression.append('nombres = :nombres')
        expression_values[':nombres'] = nombres
    if apellidos:
        update_expression.append('apellidos = :apellidos')
        expression_values[':apellidos'] = apellidos
    
    if not update_expression:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'At least one field to update is required'})
        }
    
    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression='SET ' + ', '.join(update_expression),
        ExpressionAttributeValues=expression_values,
        ReturnValues='ALL_NEW'
    )
    # Salida (json)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Alumno modificado exitosamente', 'response': response}, default=str)
    }
