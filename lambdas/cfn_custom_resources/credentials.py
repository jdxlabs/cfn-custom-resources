import boto3
import base64
import json
from botocore.exceptions import ClientError
import cfn_resource

handler = cfn_resource.Resource()

@handler.create
@handler.update
def get_credentials(event, context):
    props = event['ResourceProperties']
    secret_manager_key = props['SecretManagerKey']
    try:
        json_value = json.loads(get_secret_value(secret_manager_key))
        return {
            'Status': 'SUCCESS',
            'PhysicalResourceId': "%s/credentials" % secret_manager_key,
            'Data': {
                'Username': json_value['username'],
                'Password': json_value['password']
            }
        }
    except ValueError:
        return {
            'Status': 'FAILED',
            'Reason': 'Can''t find or retrieve secret from key %s ' % secret_manager_key
        }

@handler.delete
def on_delete(event, context):
    return {
        'Status': cfn_resource.SUCCESS
    }


# internal functions

def get_secret_value(secret_manager_key):
    client = boto3.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_manager_key)
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])
