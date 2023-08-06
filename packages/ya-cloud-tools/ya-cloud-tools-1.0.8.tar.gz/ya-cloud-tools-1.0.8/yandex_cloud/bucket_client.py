import io
from tempfile import NamedTemporaryFile
from typing import List, Optional

from botocore.exceptions import ClientError, ParamValidationError

from .logger import logger
from .object_storage import ObjectStorage

__all__ = ["ObjectStorage", "BucketClient"]


class BucketClient(ObjectStorage):
    """
    Managing the objects in Bucket.

    Instance methods short description:
       - get_list_all_objects() - Get list all objects from bucket
       - get_list_objects_generator() - Get list <=1000 objects from bucket
       - get_bytes_object() - Get object bytes format
       - upload_file() - Upload file to bucket
       - move_objects() - Move objects
       - remove_objects() - Remove objects in bucket
    """

    bucket_name = None

    def __init__(self, key_id: str, secret_key: str, bucket_name: str):
        """
        Class initialization

        :param key_id Key identifier
        :param secret_key Secret key
        :param bucket_name Name of the bucket to work with
        """
        super().__init__(key_id, secret_key)
        self.bucket_name = bucket_name

    def get_list_objects_generator(self, path: str = '', start_after: str = '') -> List[dict]:
        """
        Get list objects from bucket. (Generator)

        :param path Path
        :param start_after Return all elements after the specified value

        :return List of dictionaries containing information about objects

                Example response: [
                    {
                        'Key': 'banner_1.jpg',
                        'LastModified': datetime.datetime(2020, 6, 12, 12, 37, 2, 686000, tzinfo=tzutc()),
                        'ETag': '"a440b0e3bcdd651c18626df3374463cd"',
                        'Size': 359546,
                        'StorageClass': 'STANDARD'
                    },
                    ...,
                    ...
                ]

        """
        retry = True
        while retry:
            try:
                res = self.s3.list_objects_v2(Bucket=self.bucket_name, StartAfter=start_after, Prefix=path)
            except ClientError as exc:
                self.__validate_client_error(exc)
                break
            retry = res['KeyCount'] == 1000
            start_after = res.get('Contents', [])[-1].get('Key') if retry else ''
            yield res.get('Contents', [])

    def get_list_all_objects(self, path: str = '', limit: int = None) -> List[dict]:
        """
        Get list all objects from bucket

        :param path Path
        :param limit Response limit
        """
        list_objects = []
        logger.debug(f'Getting list all objects from bucket: {self.bucket_name}. Path: {path}')
        for result in self.get_list_objects_generator(path):
            list_objects += result
            if limit and len(result) > limit:
                break
        logger.debug(f'Received a list with information about {len(list_objects[:limit])} files.')
        return list_objects[:limit]

    def download_file(self, source_filename: str, target_filename=None, target_temp_file=False):
        """
        Get bytes object.

        :param source_filename Object name in bucket
        :return Object format bytes or None
        """
        logger.debug(f'Try getting object: {source_filename}')
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=source_filename)
        except ClientError as exc:
            return self.__validate_client_error(exc)
        if response['ContentType'] == 'application/x-directory':
            return None
        logger.debug('We got file successfully.')

        if target_filename:
            with io.FileIO(target_filename, 'w') as file:
                for i in response['Body']:
                    file.write(i)
            return target_filename

        elif target_temp_file:
            file = NamedTemporaryFile(delete=False, suffix=source_filename)
            for i in response['Body']:
                file.write(i)
            file.close()
            return file.name

        return response['Body']

    def upload_file(self, file_name: str, file_content: bytes, content_type: str = None, **kwargs):
        """
        Upload file to bucket

        :param file_name File name
        :param file_content File content
        """
        if content_type:
            kwargs['ContentType'] = content_type
        logger.debug(f'Try upload file to path: {file_name}')
        try:
            return self.s3.put_object(Bucket=self.bucket_name, Key=file_name, Body=file_content, **kwargs)
        except (ClientError, ParamValidationError) as exc:
            if exc.__class__.__name__ == 'ParamValidationError':
                return logger.error(f'{exc.args[0]}')
            return self.__validate_client_error(exc)

    def move_objects(self, out_path: str, objects_list: List[dict] = None, in_path: str = None):
        """
        Move objects.

        :param out_path: Path to move files to
        :param objects_list: List of objects to move. (Received by the `self.get_all_list()` method)
        :param in_path: Path to move files from
        :return None
        """
        def move_objects_list(objects):
            """
            Move objects list

            :param objects List of objects to move. (Received by the `self.get_all_list()` method)
            :return None
            """
            for k, object_data in enumerate(objects):
                original_object = object_data.get('Key')
                file_name = original_object.split('/')[-1]
                self.upload_file(f"{out_path}/{file_name}", self.get_bytes_object(original_object))
                self.remove_objects([original_object])
                logger.info(f"Moved {k + 1}/{len(objects)}")

        objects_list = [] if objects_list is None else objects_list
        if in_path:
            objects_list += self.get_list_all_objects(path=in_path)
        objects_list = list(set(objects_list))
        move_objects_list(objects_list)

    def remove_objects(self, remove_objects: list) -> Optional[bool]:
        """
        Remove objects from bucket

        :param remove_objects Data to remove from bucket.
            Example: ['object_name_1', 'object_name_2', ...]

        :return Execution result. True/False
        """
        objects = [{'Key': obj} for obj in remove_objects]
        logger.debug(f'Try deleting objects: {remove_objects}')
        try:
            self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects})
        except ClientError as exc:
            return self.__validate_client_error(exc)
        logger.debug('Deleted successfully.')
        return True

    @staticmethod
    def __validate_client_error(client_error: ClientError):
        """ Validate error """
        operation_map = {
            'DeleteObjects': 'Error deleting the list of objects',
            'PutObject': 'Error upload file to bucket',
            'GetObject': 'Error! The specified key does not exist'
        }

        message_code = client_error.response['Error']['Code']
        status_code = client_error.response['ResponseMetadata']['HTTPStatusCode']
        error_msg = operation_map.get(client_error.operation_name, 'Unknown error')

        logger.error(f"{error_msg}. {message_code}/HTTP {status_code}.")
