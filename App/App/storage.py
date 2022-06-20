import arrow
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class ImageStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_IMAGE_BUCKET_NAME
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_key = settings.AWS_SECRET_ACCESS_KEY
    region_name = settings.AWS_S3_REGION_NAME
    signature_version = settings.AWS_S3_SIGNATURE_VERSION


def image_file_upload(instance, filename):
    user_id = instance.user.id
    extension = filename.split('.')[-1]
    file_name = f'profile_image_of_user_{user_id}.{extension}'
    return f'media/profile_images//{user_id}/{file_name}'
