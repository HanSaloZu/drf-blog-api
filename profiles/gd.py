from django.conf import settings
from django.utils.crypto import get_random_string

from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import enum
import six


class GoogleDriveAPI:
    class GoogleDriveFilePermission(object):
        class GoogleDrivePermissionType(enum.Enum):
            USER = "user"
            GROUP = "group"
            DOMAIN = "domain"
            ANYONE = "anyone"

        class GoogleDrivePermissionRole(enum.Enum):
            OWNER = "owner"
            READER = "reader"
            WRITER = "writer"
            COMMENTER = "commenter"

        @property
        def role(self):
            return self._role

        @property
        def type(self):
            return self._type

        @property
        def value(self):
            return self._value

        @property
        def raw(self):
            result = {
                "role": self.role.value,
                "type": self.type.value
            }

            if self.value is not None:
                result["emailAddress"] = self.value

            return result

        def __init__(self, g_role, g_type, g_value=None):
            if not isinstance(g_role, self.GoogleDrivePermissionRole):
                raise ValueError(
                    "Role should be a GoogleDrivePermissionRole instance")
            if not isinstance(g_type, self.GoogleDrivePermissionType):
                raise ValueError(
                    "Permission should be a GoogleDrivePermissionType instance")
            if g_value is not None and not isinstance(g_value, six.string_types):
                raise ValueError("Value should be a String instance")

            self._role = g_role
            self._type = g_type
            self._value = g_value

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        _ANYONE_CAN_READ_PERMISSION_ = self.GoogleDriveFilePermission(
            self.GoogleDriveFilePermission.GoogleDrivePermissionRole.READER,
            self.GoogleDriveFilePermission.GoogleDrivePermissionType.ANYONE
        )

        json_keyfile_path = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
        credentials = service_account.Credentials.from_service_account_file(
            json_keyfile_path, scopes=SCOPES)

        self._permissions = (_ANYONE_CAN_READ_PERMISSION_,)
        self._drive_service = build("drive", "v3", credentials=credentials)

    def upload_file(self, path):
        media = MediaFileUpload(path, resumable=True)
        file_name = get_random_string(length=48)
        file_metadata = {
            "name": file_name,
        }
        response = self._drive_service.files().create(
            body=file_metadata, media_body=media, fields="id, webContentLink").execute()

        for p in self._permissions:
            self._drive_service.permissions().create(fileId=response["id"],
                                                     body={**p.raw}).execute()

        return response

    def delete_file(self, file_id):
        try:
            self._drive_service.files().delete(fileId=file_id).execute()
        except HttpError as e:
            if e.status_code != 404:
                raise e
