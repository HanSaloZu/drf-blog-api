from .gd import GoogleDriveAPI
from PIL import Image
from os import remove

from django.conf import settings

google_drive = GoogleDriveAPI()


def save_photo(file, profile):
    response = upload_image(file)
    profile.photo.file_id = response["id"]
    link = "https://drive.google.com/uc?id=" + str(response["id"])
    profile.photo.link = link
    profile.user.save()
    return link


def upload_image(file):
    image = Image.open(file)
    resized_image = image.resize((300, 300))
    path = settings.MEDIA_ROOT / file.name
    resized_image.save(path,
                       quality="web_maximum", subsampling=0)
    response = google_drive.upload_file(path)
    remove(path)
    return response


def delete_image(file_id):
    google_drive.delete_file(file_id)
