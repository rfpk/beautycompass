import os
import uuid
from PIL import Image
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile


def remove_exif_data(image):
    image_opened = Image.open(image)

    image_io = BytesIO()
    image_opened.save(image_io, image_opened.format)

    image_file = InMemoryUploadedFile(
        file=image_io,
        field_name=None,
        name=image.name,
        content_type=image.content_type,
        size=image.size,
        charset=None
    )

    return image_file


def create_unique_name(filename: str, path: str):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4().hex, ext)
    while os.path.exists(settings.MEDIA_ROOT / f'{path}' / filename):
        filename = "%s.%s" % (uuid.uuid4().hex, ext)

    return os.path.join(path, filename)


