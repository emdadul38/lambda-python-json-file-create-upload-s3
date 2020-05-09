# Write JSON file and upload on s3

It's the process read data from Dynamodb and write data into different format file and upload on s3 bucket

## 1. Tmp Directory and file name

```python
TMP_DIR = "/tmp/"
file_name = "file_name_to_create_tmp.json"
tmp = os.path.join(TMP_DIR, file_name)
```

## 2. Boto3 Resource for Dynamodb and S3

```python
dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3', region_name='us-west-1')
```

## 3. Dynamodb Scan and read Data

```python
table = dynamodb.Table('pet-profile')
resource = table.scan()
data = resource['Items']
```

## 4. Write data into file

```python
if not os.path.exists(tmp):
    with open(tmp, "w",  encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4,  cls=DecimalEncoder)
```

## 5. Finally, Upload file on S3 Bucket

```python
s3_file = os.path.join('FOLDER_NAME', 'FILE_NAME.json')
s3.meta.client.upload_file(tmp, BUCKET_NAME, s3_file)
```

## Helper class to convert a DynamoDB item to JSON.
```python
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
```
