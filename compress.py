from os import getenv
from io import BytesIO

from urllib.parse import unquote_plus
from pathlib import Path
from PIL import Image

import boto3


def compress_image(filename, bucketname, output_path, mode, palette):
    client = boto3.client('s3')
    response = client.get_object(Bucket=bucketname, Key=filename)
    data = response["Body"].read()
    p = Path(filename)

    with BytesIO(data) as img_data:
        with Image.open(img_data) as img:
            # Basic optimization dropping the data complexity
            with img.convert(mode=mode, palette=palette) as converted_img:
                with BytesIO() as img_writer:
                    # Further optimization by using zlib compression and the
                    # optimized PNG writer
                    converted_img.save(
                        img_writer,
                        format='png',
                        optimize=True,
                        compress_level=9)
                    img_writer.seek(0)
                    client.put_object(
                        ACL='public-read',
                        Bucket=bucketname,
                        Body=img_writer,
                        Key='{}/{}'.format(output_path, p.name))


def lambda_handler(event, context):
    for record in event['Records']:
        # So... before handing off the key to the lambda function S3
        # URI encodes which is why the unquote_plus is here
        compress_image(
            unquote_plus(record['s3']['object']['key']),
            record['s3']['bucket']['name'],
            getenv('OUTPUT_IMAGE_PATH'),
            getenv('IMAGE_MODE'),
            getenv('IMAGE_PALETTE'))
