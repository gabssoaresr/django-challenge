import os
import boto3
import string
import secrets
from django.http import HttpResponse
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class CustomS3Boto3Storage:
    def __init__(
        self, 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        bucket_name=os.getenv('AWS_STORAGE_BUCKET_NAME'),
        region_name=os.getenv('AWS_STORAGE_BUCKET_REGION_NAME')
    ):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_path, key):
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, key)
            return True
        except ClientError as e:
            raise ClientError("Erro ao fazer upload do arquivo") from e 

    def upload_fileobj(self, file_obj, key):
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, key)
            return True
        except ClientError as e:
            raise ClientError("Erro ao fazer upload do arquivo") from e 

    def get_download_url(self, key):
        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=3600 
            )
            return url
        except ClientError as e:
            raise ClientError("Erro ao gerar URL de download do arquivo") from e


    def delete_object(self, key):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return True
        except ClientError as e:
            raise ClientError("Erro ao excluir o objeto") from e
        
    def generate_random_filename_string(self, extension: str, length=10):
        characters = string.ascii_letters + string.digits
        random_string = "".join(secrets.choice(characters) for _ in range(length))
        return random_string + "." + extension
