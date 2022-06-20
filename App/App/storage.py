from django.conf import settings
from django.db.models import Model
from storages.backends.s3boto3 import S3Boto3Storage


class ImageStorage(S3Boto3Storage):
    bucket_name: str = settings.AWS_STORAGE_IMAGE_BUCKET_NAME
    access_key: str = settings.AWS_ACCESS_KEY_ID
    secret_key: str = settings.AWS_SECRET_ACCESS_KEY
    region_name: str = settings.AWS_S3_REGION_NAME
    signature_version: str = settings.AWS_S3_SIGNATURE_VERSION


def image_file_upload(instance: Model, filename: str) -> str:
    user_id: int = instance.user.id
    extension: str = filename.split(".")[-1]
    file_name: str = f"profile_image_of_user_{user_id}.{extension}"
    return f"media/profile_images//{user_id}/{file_name}"
