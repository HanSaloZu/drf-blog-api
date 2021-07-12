from django.conf import settings
from django.utils.crypto import get_random_string

from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import enum


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


class GoogleDriveFilePermission:
    @property
    def role(self):
        return self._role

    @property
    def type(self):
        return self._type

    @property
    def raw(self):
        return {
            "role": self.role.value,
            "type": self.type.value
        }

    def __init__(self, g_role, g_type):
        if not isinstance(g_role, GoogleDrivePermissionRole):
            raise ValueError(
                "Role should be a GoogleDrivePermissionRole instance")
        if not isinstance(g_type, GoogleDrivePermissionType):
            raise ValueError(
                "Permission should be a GoogleDrivePermissionType instance")

        self._role = g_role
        self._type = g_type


class GoogleDriveAPI:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']

        json_keyfile_path = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE
        credentials = service_account.Credentials.from_service_account_file(
            json_keyfile_path, scopes=SCOPES)

        self._drive_service = build("drive", "v3", credentials=credentials)

    def upload_file(self, path, permissions=()):
        media = MediaFileUpload(path, resumable=True)
        file_name = get_random_string(length=48)
        file_metadata = {
            "name": file_name,
        }
        response = self._drive_service.files().create(
            body=file_metadata, media_body=media, fields="id, webContentLink").execute()

        if not permissions:
            _ANYONE_CAN_READ_PERMISSION_ = GoogleDriveFilePermission(
                GoogleDrivePermissionRole.READER,
                GoogleDrivePermissionType.ANYONE
            )
            permissions = (_ANYONE_CAN_READ_PERMISSION_,)

        for p in permissions:
            if not isinstance(p, GoogleDriveFilePermission):
                raise ValueError(
                    "Permissions should be a list or a tuple of GoogleDriveFilePermission instances")
            self._drive_service.permissions().create(fileId=response["id"],
                                                     body={**p.raw}).execute()

        return response

    def delete_file(self, file_id):
        try:
            self._drive_service.files().delete(fileId=file_id).execute()
        except HttpError as e:
            if e.status_code != 404:
                raise e
