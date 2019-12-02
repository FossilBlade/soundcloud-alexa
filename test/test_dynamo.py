import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

ddb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000',region_name='us-east-1',aws_access_key_id="key",
                          aws_secret_access_key="anything")
table = ddb.Table('user_session')


response = table.query(
    KeyConditionExpression=Key('userId').eq("dsafasdfadsfsdaf")
)

for i in response['Items']:
    print(json.dumps(i, cls=DecimalEncoder))