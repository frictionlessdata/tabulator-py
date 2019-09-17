# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import boto3
import pytest
import string
import random
from moto import mock_s3
from tabulator import Stream

# Setup

os.environ['S3_ENDPOINT_URL'] = 'http://localhost:5000'


# Stream

def test_stream_s3_1(s3_client, bucket):
    assert True


def test_stream_s3_2(s3_client, bucket):
    assert True


# Fixtures

@pytest.fixture(scope='module')
def s3_client():
    s3_server = mock_s3()
    s3_server.start()
    s3_client = boto3.client('s3', endpoint_url=os.environ.get('S3_ENDPOINT_URL'))
    yield s3_client
    s3_server.stop()


@pytest.fixture
def bucket(s3_client):
    bucket = 'bucket_%s' % ''.join(random.choice(string.digits) for _ in range(16))
    s3_client.create_bucket(Bucket=bucket, ACL='public-read')
    return bucket
