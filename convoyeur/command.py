import sys
import os
import argparse
import logging
from urlparse import urlparse

from . import __version__
from . import listener
from . import uploader
from .executor import ThreadPoolExecutor
from .processor import EventProcessor
from .process import Process


logger = logging.getLogger(__name__)


def positive_int(x):
    x = int(x)
    if x <= 0:
        raise ValueError('Integer {} must be strictly positive'.format(x))

    return x


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        description='Process that reads file names to upload')

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input to read to get file names')

    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output location to upload the files')

    parser.add_argument(
        '-N', '--nb_processes',
        type=positive_int,
        default=1,
        help='Number of concurrent upload processes')

    parser.add_argument(
        '-V', '--version',
        action='store_true',
        default=False)

    return parser.parse_args(arguments)


def parse_input(conf):
    parsed = urlparse(conf)
    if parsed.scheme != 'pipe':
        raise NotImplementedError('{} is not a supported input'.format(
            parsed.scheme))

    return listener.NamedPipeListener(
        os.path.join(parsed.netloc, parsed.path))


UPLOADERS = {
    'local': uploader.LocalUploader,
    's3': uploader.S3Uploader,
}


def parse_output(conf):
    parsed = urlparse(conf)
    if parsed.scheme not in UPLOADERS:
        raise NotImplementedError('{} is not a supported uploader'.format(
            parsed.scheme))

    path = os.path.join(parsed.netloc, parsed.path.strip('/'))
    return UPLOADERS[parsed.scheme](path)


def main():
    options = parse_arguments(sys.argv[1:])
    if options.version:
        print(__version__)
        return 0

    listener = parse_input(options.input)
    uploader = parse_output(options.output)
    uploader = uploader(EventProcessor(lambda ev: ev.split('\t')[1:]))
    executor = ThreadPoolExecutor(options.nb_processes)

    process = Process(listener, uploader, executor)
    process.run()
