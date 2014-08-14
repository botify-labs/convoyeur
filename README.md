# Overview

`convoyeur` reads the name of files from a listening interface such as a
named pipe and uploads the file on a remote location such as a S3 bucket.

It relies on the composition of three concepts:

- Listener
- Processor
- Uploader

A listener listens on a interface to read file names. A processor applies
functions to a file name. It can check the type of a file, its size, or notify
that the file was written.

# Quickstart

The default configuration listens on a named pipe and sends logs to a S3
bucket. You need to set:

- The `path` of the named pipe.
- The name of the S3 bucket.
- The AWS credentials with sufficient permissions to the S3 bucket.

It is also recommended to configure the logging.

Run [watchfiles](https://github.com/botify-labs/watchfiles):

```sh
$ ./watchfiles /data/logs /tmp/new_logs.fifo
```

Then make `convoyeur` listen to the named pipe:

```sh
$ convoyeur -i pipe:///tmp/new_logs.fifo -o s3://bucket/path/to/dir --nb_processes=8
```
