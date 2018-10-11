import boto3
import base64
import json
from botocore.exceptions import ClientError
import cfn_resource

handler = cfn_resource.Resource()

@handler.create
@handler.update
def strutils(event, context):
    props = event['ResourceProperties']
    string = props['String']
    func = props['Function']
    if 'Args' in props:
        args = props['Args']
    else:
        args = []

    physical_id = "%s/str/%s/func" % (string, func)
    if (args):
        args_str = '-'.join(args)
        physical_id = "%s/%s/args" % (physical_id, args_str)

    try:
        if (func == 'upper'):
            res = string.upper()
        elif (func == 'lower'):
            res = string.lower()
        elif (func == 'replace'):
            res = string.replace(args[0], args[1])

        return {
            'Status': 'SUCCESS',
            'PhysicalResourceId': physical_id,
            'Data': {
                'Res': res
            }
        }
    except ValueError:
        return {
            'Status': 'FAILED',
            'Reason': 'Error during the treatment of the string %s with the function %s (%s) ' % (string, func, args)
        }

@handler.delete
def on_delete(event, context):
    return {
        'Status': cfn_resource.SUCCESS
    }
