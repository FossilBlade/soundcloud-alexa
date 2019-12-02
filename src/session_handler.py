import boto3
import json
import decimal
import os
from boto3.dynamodb.conditions import Key, Attr

session_table_name = 'UserSession'

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

endpoint_url = os.environ.get('DDB_ENDPOINT_URL') or None

if os.environ.get('AWS_ACCESS_KEY_ID') and os.environ.get('AWS_ACCESS_KEY_SECRET') and os.environ.get('AWS_REGION'):
    ddb = boto3.resource('dynamodb',endpoint_url=endpoint_url,
                         aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY_SECRET'),
                         region_name=os.environ.get('AWS_REGION'))
else:
    ddb = boto3.resource('dynamodb',endpoint_url=endpoint_url)

def get_user_queue(user_id):
    table = ddb.Table(session_table_name)

    response = table.query(
        ProjectionExpression="queueState",
        KeyConditionExpression=Key('userId').eq(user_id)
    )
    items = response['Items']

    # {
    #     "userId": "dsafasdfadsfsdaf",
    #     "queueState": {
    #         "current": "13131",
    #         "queue": [],
    #         "history": []
    #     }
    # }

    if len(items) != 1:
        return {}
    else:
        return items[0]['queueState']


def update_user_queue(user_id, queue_state):
    table = ddb.Table(session_table_name)

    response = table.update_item(
        Key={
            'userId': user_id
        },
        UpdateExpression="set queueState = :q",
        ExpressionAttributeValues={
            ':q': queue_state

        },
        ReturnValues="UPDATED_NEW"
    )

    return response
