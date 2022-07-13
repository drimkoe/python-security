from secrets import token_bytes
import boto3
import uuid
from cryptography.fernet import Fernet

def generate_key():
    key_name = str(uuid.uuid4())
    key_value = token_bytes(16)
    aws_session = boto3.session.Session()
    aws_secrets_client = aws_session.client(service_name='secretsmanager',region_name='us-west-2')
    
    response = aws_secrets_client.create_secret(Name=key_name,SecretBinary=key_value)

    with open('keyname.txt','w') as fw:
        fw.write(key_name)

    print(response)

def generate_symmetric_key():
    key_name = str(uuid.uuid4())
    key_value = Fernet.generate_key()
    aws_session = boto3.session.Session()
    aws_secrets_client = aws_session.client(service_name='secretsmanager',region_name='us-west-2')
    
    response = aws_secrets_client.create_secret(Name=key_name,SecretBinary=key_value)

    with open('symmetric_key.txt','w') as fw:
        fw.write(key_name)

    print(response)

generate_symmetric_key()
