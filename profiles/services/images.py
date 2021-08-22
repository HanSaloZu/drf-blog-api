from PIL import Image
from os import remove

from django.conf import settings

from .google_drive_api import GoogleDriveAPI

google_drive = GoogleDriveAPI()


def upload_image(file):
    # Save file temporarily in the media folder
    image = Image.open(file)
    path = settings.MEDIA_ROOT / file.name
    image.save(path, quality="web_maximum", subsampling=0)

    response = google_drive.upload_file(path)
    remove(path)  # Remove file from media folder

    return response


def update_image(instance, file):
    if instance.file_id != "":
        google_drive.delete_file(instance.file_id)

    response = upload_image(file)
    link = "https://drive.google.com/uc?id=" + str(response["id"])

    instance.file_id = response["id"]
    instance.link = link
    instance.save()

    return link
