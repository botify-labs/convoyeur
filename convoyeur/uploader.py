import os.path
import logging

import boto.s3
from boto.s3.connection import S3Connection


from .processor import AbstractProcessor


logger = logging.getLogger(__name__)
DEFAULT_PATH = '/'


class LocalUploader(AbstractProcessor):
    def __init__(self, path):
        super(LocalUploader, self).__init__()

        if not os.path.isdir(path):
            raise ValueError('{} must be a directory'.format(path))

        self._path = path

    def copy_file(self, src, dst):
        import shutil

        shutil.copyfile(src, dst)

    def process(self, event):
        basedir, filename = super(LocalUploader, self).process(event)
        src = os.path.join(basedir, filename)
        dst = os.path.join(self._path, filename)
        logger.info('copying file {} to {}'.format(src, dst))
        self.copy_file(src, dst)
        return basedir, filename


class S3Uploader(AbstractProcessor):
    def __init__(self, path):
        super(S3Uploader, self).__init__()

        bucket_name, path = self.split_path(path)
        self._bucket_name = bucket_name
        self._path = path

        self._s3 = S3Connection()
        self._bucket = self._s3.get_bucket(bucket_name)

    def split_path(self, path):
        result = path.strip('/').split('/', 1)
        if len(result) == 1:
            if result == '':
                raise ValueError('incorrect bucket name "{}"'.format(result))

            return result, '/'

        return (result[0], result[1])

    def upload_file(self, src, dst):
        from boto.s3.key import Key

        key = Key(self._bucket)
        key.name = dst
        try:
            key.set_contents_from_filename(src)
        except:
            raise RuntimeError('cannot upload file {} on {}'.format(
                self._bucket_name,
                src))

    def process(self, event):
        basedir, filename = super(S3Uploader, self).process(event)
        src = os.path.join(basedir, filename)
        dst = filename
        logger.info('uploading file {} to {}'.format(
            src,
            's3://' + '/'.join([self._bucket_name, dst])))

        self.upload_file(src, dst)

        return basedir, filename
