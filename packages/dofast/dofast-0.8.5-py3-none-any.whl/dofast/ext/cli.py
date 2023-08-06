#!/usr/bin/env python
from typing import List, Tuple, Union

import codefast as cf

from dofast.oss import Bucket
from dofast.utils import DeeplAPI
from dofast.vendor.command import Command, Context

cf.logger.level = 'info'


class OSSCommand(Command):
    '''OSS manager'''
    def __init__(self):
        super().__init__()
        self.name = 'oss'
        self.subcommands = [['list_files', 'list', 'ls', 'l'],
                            ['del', 'delete', 'rm'], ['up', 'upload', 'u'],
                            ['dw', 'd', 'download', 'down']]

        self.cli = Bucket()
        self.description = 'OSS manager.'

    def upload(self, files: List[str]):
        for f in files:
            cf.info('uploading file {}'.format(f))
            self.cli.upload(f)

    def download(self, files: List[str]):
        for f in files:
            cf.info('downloading file {}'.format(f))
            f = cf.io.basename(f)
            self.cli.download(f, f)

    def list_files(self, sort_by_size: bool = False):
        cf.info(self.cli.url_prefix)
        if sort_by_size:
            self.cli.list_files_by_size()
        else:
            self.cli.list_files()


class DeeplTranlationCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = 'deepl'
        self.description = 'Translate Text or Document with DeepL API.'

    def _process(self, texts: List[str]) -> str:
        cli = DeeplAPI()
        if not texts:
            cli.stats
            return
        _f = lambda t: cli.document(t) if cf.io.exists(t) else cli.translate(t)
        for cand in texts:
            cf.info('DeepL translating: {}'.format(cand))
            _f(cand)


class FileInfo(Command):
    def __init__(self):
        super().__init__()
        self.name = 'fileinfo'
        self.description = 'Query audio file information.'

    def _process(self, files: List[str]):
        for f in files:
            cf.info('Query file info: {}'.format(f))
            info = cf.io.info(f)
            for key in ('bit_rate', 'channel_layout', 'channels',
                        'codec_tag_string', 'codec_long_name', 'codec_name',
                        'duration', 'filename', 'format_name', 'sample_rate',
                        'size', 'width'):
                print('{:<20} {}'.format(key, info.get(key, None)))


def app():
    cont = Context()
    cont.add_command('oss', OSSCommand)
    cont.add_command('deepl', DeeplTranlationCommand)
    cont.add_command(['fileinfo', 'fi'], FileInfo)
    cont.execute()
