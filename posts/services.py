from profiles.services.google_drive_api import GoogleDriveAPI
from profiles.services.images import update_image

from .models import Attachment

google_drive = GoogleDriveAPI()


def delete_post_attachments(post):
    attachments = Attachment.objects.all().filter(post=post)

    for attachment in attachments:
        google_drive.delete_file(attachment.file_id)
        attachment.delete()


def create_post_attachment(post, file):
    attachment = Attachment.objects.create(
        post=post, file_id="", link="")
    update_image(attachment, file)


def delete_post(post):
    delete_post_attachments(post)
    post.delete()


def get_post_attachments_list(post):
    return list(Attachment.objects.all().filter(
        post=post
    ).values_list("link", flat=True))
