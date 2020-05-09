import os
import json
import boto3
import logging
import decimal
import tempfile

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
TMP_DIR = "/tmp/"
BUCKET_NAME = 'BUCKET_NAME'

def lambda_handler(event, context):
    # TODO implement
    try:
        file_name = "file_name_to_create_tmp.json"
        tmp = os.path.join(TMP_DIR, file_name)

         # this will create dynamodb resource object and
        # here dynamodb is resource name
        dynamodb = boto3.resource('dynamodb')
        # Resource S3 with Region Name
        s3 = boto3.resource('s3', region_name='us-west-1')

        # this will search for dynamoDB table
        # your table name may be different
        table = dynamodb.Table('pet-profile')
        resource = table.scan()
        data = resource['Items']
        try:

            if not os.path.exists(tmp):
                with open(tmp, "w",  encoding='utf-8') as f:
                    final_data = {
                        "store": data
                    }

                    json.dump(final_data, f, ensure_ascii=False, indent=4,  cls=DecimalEncoder)

                # Full path where file create
                s3_file = os.path.join('FOLDER_NAME', 'FILE_NAME.json')

                # Upload file to the bucket
                s3.meta.client.upload_file(tmp, BUCKET_NAME, s3_file)

            return {
                'statusCode': 200,
                'body': json.loads(json.dumps(data,  cls=DecimalEncoder))
            }
        except Exception as error:
            logger.exception(error)

    except Exception as error:
        logger.exception(error)
        response = {
            'status': 500,
            'error': {
                'type': type(error).__name__,
                'description': str(error),
            },
        }


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
