import datetime
import functools
import logging
import os
import pathlib
import sys
from typing import TypedDict

import click
import oss2

from yucebio_uploader.base import BaseUploader


class OSSConfig(TypedDict):
    access_key_id: str
    access_key_secret: str
    region: str
    bucket: str

class Uploader(BaseUploader):
    PLATFROM = 'ali'
    ALIAS_NAME = ['bcs', 'oss', 'ali']

    def __init__(self) -> None:
        super().__init__()
        self._auth = None
        self._bucket = None

    @property
    def config(self):
        return self._config('oss', {})

    def configure(self):
        access_id = click.prompt("Please Input ACCESS KEY ID")
        access_secrect = click.prompt("Please Input ACCESS KEY SECRECT")
        region = click.prompt("Please Input Region", default='cn-shenzhen')
        bucket = click.prompt("Please Input Bucket name", default='yucebio')
        endpoint = click.prompt("Please Input Endpoint", default=f"https://oss-{region}.aliyuncs.com")

        self._config['oss'] = {
            "access_key_id": access_id,
            "access_key_secret": access_secrect,
            "region": region,
            "bucket": bucket,
            "endpoint": endpoint
        }
        self._config.reload()

    @property
    def oss_config(self) -> OSSConfig:
        if not self.config:
            self.configure()
        return self.config

    @property
    def endpoint(self) -> str:
        return self.oss_config['endpoint'] or f"https://oss-{self.oss_config['region']}.aliyuncs.com"

    @property
    def auth(self) -> oss2.Auth:
        if not self._auth:
            self._auth = oss2.Auth(self.oss_config["access_key_id"], self.oss_config['access_key_secret'])
        return self._auth

    @property
    def bucket(self) -> oss2.Bucket:
        if not self._bucket:
            self._bucket = oss2.Bucket(self.auth, self.endpoint, self.oss_config['bucket'])
        return self._bucket

    def upload(self, local: str, remote: str, recursive: bool = False) -> str:
        if not os.path.exists(local):
            raise FileNotFoundError(local)

        def percentage(byte_size, total_bytes):
            if total_bytes:
                rate = int(100 * (float(byte_size) / float(total_bytes)))
                print(click.style(f'\rUploaded {rate}%:', fg='yellow') + click.style('#' * rate, fg='green'), end="")
                sys.stdout.flush()

        bucket_name = self.oss_config['bucket']
        if remote.startswith('oss://'):
            bucket_name = remote[6:].split('/')[0]
            remote = remote[(6+len(bucket_name)+1):]

        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name)

        key = '/'.join(pathlib.Path(remote).parts)
        oss_path = f"oss://{bucket.bucket_name}/{key}"
        click.secho(f"开始上传文件{local} ==> {oss_path}", fg='green')

        # 检查文件是否存在
        if bucket.object_exists(key):
            # 阿里云的etag与md5不是一个东西，不能作为判断依据
            meta: oss2.models.GetObjectMetaResult = bucket.get_object_meta(key)
            logging.info(f"oss file already exist! etag: {meta.etag}, size: {meta.content_length}")
            # md5 = self.md5(local)
            # if meta.etag.lower() == md5:
            #     logging.info(f"remote file [{remote}][md5: {meta.etag}] exists!! ")
            #     return f"oss://{bucket.bucket_name}/{key}"
            # else:
            #     logging.info(f"remote file [{remote}][etag: {meta.etag}][md5: {md5}]!! ")
            return oss_path
            

        logging.info(f"start upload file: {local} ==> {remote}")
        # self.bucket.put_object_from_file(key, local, progress_callback=percentage)
        oss_path = self.multipart_upload(bucket, local, key)
        logging.info(f"{oss_path} file upload success.")

        return oss_path

    def exists(self, remote: str):
        key = '/'.join(pathlib.Path(remote).parts)

        bucket_name = self.oss_config['bucket']
        if remote.startswith('oss://'):
            bucket_name = remote[6:].split('/')[0]
            remote = remote[(6+len(bucket_name)+1):]

        bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name)
        try:
            return bucket.object_exists(key)
        except:
            return False

    def multipart_upload(self, bucket: oss2.Bucket, local: str, key: str):

        def multipart_percentage(start: datetime.datetime, offset: int, total_size: int, byte_size: int, chunk_size: int):
            size = os.get_terminal_size(sys.stdout.fileno()).columns
            timedelta = datetime.datetime.now() - start

            total_seconds = timedelta.total_seconds()
            upload_size = byte_size + offset
            rate = int(100 * (upload_size / float(total_size)))

            speed = float(upload_size) / 1024 / 1024 / total_seconds    # x kb/s
            prefix = f"Uploaded {rate}% [{speed:0.2f} Mb/s]:"

            # 进度条宽度自适应
            usable_width = size - len(prefix)
            width = 100
            if usable_width <= width:
                width = usable_width - 1
            str_shape = '#' * int(rate * width / 100)

            if chunk_size:
                print(click.style(f'\r{prefix}', fg='yellow') + click.style(str_shape, fg='green'), end="", flush=True)


        init_multipart_upload_result = bucket.init_multipart_upload(key)
        total_size = os.path.getsize(local)

        # 根据总大小和用户期望分片大小（默认为10*1024*1024）计算合适的分片大小
        chunk_size = oss2.determine_part_size(total_size)
        parts = []
        start = datetime.datetime.now()
        with open(local, 'rb') as r:
            part_number = 1
            offset = 0
            while offset < total_size:
                # print("begin part upload", part_number, offset, chunk_size, total_size, f"oss://{bucket.bucket_name}/{key}")
                size_to_upload = min(chunk_size, total_size - offset)

                data = oss2.SizedFileAdapter(r, size_to_upload)
                result = bucket.upload_part(key, init_multipart_upload_result.upload_id, part_number, data, progress_callback=functools.partial(multipart_percentage, start, offset, total_size))
                parts.append(oss2.models.PartInfo(part_number, result.etag))

                offset += size_to_upload
                part_number += 1

                # print("upload part", key, part_number, size_to_upload, result.etag, init_multipart_upload_result.upload_id)

        bucket.complete_multipart_upload(key, init_multipart_upload_result.upload_id, parts)
        return f"oss://{bucket.bucket_name}/{key}"
