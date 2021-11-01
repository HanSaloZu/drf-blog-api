from os import remove

from django.conf import settings
from PIL import Image

from .google_drive_api import GoogleDriveAPI

google_drive = GoogleDriveAPI()


def update_instance_image(instance, file):
    if instance.file_id != "":
        google_drive.delete_file(instance.file_id)

    file_id, link = upload_image(file)

    instance.file_id = file_id
    instance.link = link
    instance.save()

    return link


def upload_image(file):
    path = save_image_in_media_folder(file)

    file_id, link = google_drive.upload_file(path)
    remove(path)

    return file_id, link


def save_image_in_media_folder(file):
    image = Image.open(file)
    path = settings.MEDIA_ROOT / file.name

    if file.content_type == "image/gif":
        image.save(path, optimize=True, quality=45,
                   loop=0, save_all=True, disposal=2)
    else:
        image.save(path, optimize=True, quality=45)

    return path
