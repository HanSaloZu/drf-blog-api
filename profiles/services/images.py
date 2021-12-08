from os import remove

from django.conf import settings
from django.core.files.storage import default_storage
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
        save_gif(file, path)
    else:
        image.save(path, optimize=True, quality=45)

    return path


def save_gif(file, path):
    with default_storage.open(path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
