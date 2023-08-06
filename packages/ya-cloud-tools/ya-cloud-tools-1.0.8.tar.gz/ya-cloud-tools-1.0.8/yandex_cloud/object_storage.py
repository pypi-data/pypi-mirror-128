# Library for managing the ObjectStorage service in YandexCloud.

from boto3.session import Session
from botocore.exceptions import ClientError

from .logger import logger

__all__ = ["ObjectStorage"]


class ObjectStorage:
    """
    Managing the Buckets in ObjectStorage.

    Instance methods short description:
        - get_bucket_client() - Initial BucketClient instance.
        - check_auth() - Check authorization state.
    """

    def __init__(self, key_id: str, secret_key: str):
        """
        Class initialization

        :param key_id ID of the access key
        :param secret_key Secret key
        """
        self.authorized = False
        self.KEY_ID = key_id
        self.SECRET_KEY = secret_key

        self.s3 = Session().client(service_name='s3', aws_access_key_id=key_id,
                                                 endpoint_url='https://storage.yandexcloud.net',
                                                 aws_secret_access_key=secret_key)
        logger.info("Start authorization ...")
        self.check_auth()

    @staticmethod
    def get_bucket_client(key_id: str, secret_key: str, bucket_name: str) -> "BucketClient":
        """
        Get bucket client

        :param key_id Key identifier
        :param secret_key Secret key
        :param bucket_name Name of the bucket to work with

        :return BucketClient instance
        """
        from .bucket_client import BucketClient
        return BucketClient(key_id, secret_key, bucket_name)

    def check_auth(self) -> bool:
        """
        Check authorization state

        To check authorization, use the `s3.list_buckets()` method
        """
        try:
            self.s3.list_buckets()
        except ClientError:
            self.authorized = False
            logger.error("Authorization failed!")
        self.authorized = True
        logger.info("Authorization success!")
        return self.authorized
