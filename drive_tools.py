"""
Functions for interact with Google Drive

"""
from pathlib import Path
from typing import Optional, Union
import pickle
import os.path
from pprint import pprint
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

# TODO change all none domain to my_
# TODO search for folders as files and seperate functions for folders as drives


def google_creds() -> object:
    """
       This function handles auth and service for google drive api v3 and minimal sheets api.

       Returns:

       """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.activity',
              'https://www.googleapis.com/auth/spreadsheets'
              ]

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def drive_service() -> object:
    """
    This function negotiates access to Google Drive.

    Returns:
        object: Drive API service instance.

    """
    g_drive_service = build('drive', 'v3', credentials=google_creds())

    return g_drive_service


def sheets_service() -> object:
    """
    This function negotiates access to Google Sheets.

    Returns:
        object: Google Sheets API service instance.

    """
    g_sheets_service = build('sheets', 'v4', credentials=google_creds())

    return g_sheets_service


def no_cache_discovery_service():
    service = build('drive', 'v3', credentials=google_creds(), cache_discovery=False)
    return service


def list_my_folders_by_searching_files() -> list:
    """
    Creates a list of all the folders that api Oauth user owns.

    Returns:
        list: List of folders. Each folder returns a dict of data.

    """
    page_token = None
    getting_files = True
    my_folders = []  # all the folders i have access to

    while getting_files:
        if not page_token:
            response = drive_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                    fields="*",
                                                    spaces='drive').execute()
        else:
            response = drive_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                    fields="*",
                                                    spaces='drive',
                                                    pageToken=page_token).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['files']  # Drive api refers to files and folders as files.
        for folder in folders:
            my_folders.append(folder)

    return my_folders


def list_domain_folders_by_searching_files() -> list:
    """
    Creates a list of all the domain shared folders that api Oauth user has access to.

    Returns:
        list: List of domain shared folders. Each folder returns a dict of data.

    """

    page_token = None
    getting_files = True
    domain_folders = []  # all the domain shared folders i have access to.

    while getting_files:
        if not page_token:
            response = no_cache_discovery_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                                 supportsAllDrives=True,
                                                                 includeItemsFromAllDrives=True,
                                                                 corpora='allDrives',
                                                                 fields="*",
                                                                 ).execute()
        else:
            response = no_cache_discovery_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                                 supportsAllDrives=True,
                                                                 includeItemsFromAllDrives=True,
                                                                 corpora='allDrives',
                                                                 fields="*",
                                                                 pageToken=page_token
                                                                 ).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['files']
        for folder in folders:
            domain_folders.append(folder)

    return domain_folders


def list_domain_folders_by_searching_drives():
    """
    Creates a list of all the domain shared folders that api Oauth user has access to.

    Returns:
        list: List of domain shared folders. Each folder returns a dict of data.

    """

    page_token = None
    getting_files = True
    domain_folders = []  # all the domain shared folders i have access to.

    while getting_files:
        if not page_token:
            # TODO test with and with out fields
            response = no_cache_discovery_service().drives().list(useDomainAdminAccess=True,
                                                                  fields="*",
                                                                  ).execute()
        else:
            response = no_cache_discovery_service().drives().list(useDomainAdminAccess=True,
                                                                  fields="*",
                                                                  pageToken=page_token
                                                                  ).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['drives']
        for folder in folders:
            domain_folders.append(folder)

    return domain_folders


def find_my_folder_by_name_by_searching_files(folder_name: str) -> Union[bool, dict]:
    """
    Search through all the folders that the Oauth user owns. If the folder_name is found it returns a dict of
    data about the folder.

    Args:
        folder_name: Name of the Google Drive folder.

    Returns:
        bool, dict: If folder_name is found it returns a dict. If the folder name is not found it returns False.

    """
    page_token = None
    getting_files = True
    folder_data = False

    while getting_files:
        if not page_token:
            response = drive_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                    fields="*").execute()
        else:
            response = drive_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                    fields="*",
                                                    pageToken=page_token).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['files']  # Drive api refers to files and folders as files.
        for folder in folders:
            if folder_name == folder["name"]:
                folder_data = folder
                getting_files = False

    return folder_data


def find_domain_folder_by_name_by_searching_files(folder_name: str) -> Union[bool, dict]:
    """
    Search through all the domain folders that the Oauth user has access to. If the folder_name is found it returns a
    dict of data about the folder.

    Args:
        folder_name: Name of the Google Drive folder.

    Returns:
        bool, dict: If folder_name is found it returns a dict. If the folder name is not found it returns False.

    """
    page_token = None
    getting_files = True
    folder_data = False

    while getting_files:
        if not page_token:
            # TODO Change this to all drives like list_domain_folders()
            response = no_cache_discovery_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                                 supportsAllDrives=True,
                                                                 includeItemsFromAllDrives=True,
                                                                 corpora='allDrives',
                                                                 fields="*").execute()
        else:
            response = no_cache_discovery_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                                 supportsAllDrives=True,
                                                                 includeItemsFromAllDrives=True,
                                                                 corpora='allDrives',
                                                                 fields="*",
                                                                 pageToken=page_token).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['files']  # Drive api refers to files and folders as files.
        for folder in folders:
            if folder_name == folder["name"]:
                folder_data = folder
                getting_files = False

    return folder_data


def find_domain_folder_by_name_by_searching_drives(folder_name: str) -> Union[bool, dict]:
    """
    Search through all the domain folders that the Oauth user has access to. If the folder_name is found it returns a
    dict of data about the folder.

    Args:
        folder_name: Name of the Google Drive folder.

    Returns:
        bool, dict: If folder_name is found it returns a dict. If the folder name is not found it returns False.

    """
    page_token = None
    getting_files = True
    folder_data = False

    while getting_files:
        if not page_token:
            response = no_cache_discovery_service().drives().list(useDomainAdminAccess=True,
                                                                  fields="*").execute()
        else:
            response = no_cache_discovery_service().drives().list(useDomainAdminAccess=True,
                                                                  fields="*",
                                                                  pageToken=page_token).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['drives']  # Drive api refers to files and folders as files.
        for folder in folders:
            if folder_name == folder["name"]:
                folder_data = folder
                getting_files = False

    return folder_data


def find_domain_folder_by_id_by_searching_files(folder_id: str) -> Union[bool, dict]:
    """
    Search through all the domain folders that the Oauth user has access to. If the folder_id is found it returns a
    dict of data about the folder.

    Args:
        folder_id: Google Drive folder id.

    Returns:
        bool, dict: If folder_id is found it returns a dict. If the folder id is not found it returns False.

    """
    page_token = None
    getting_files = True
    folder_data = False

    while getting_files:
        if not page_token:
            response = drive_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                    corpora='domain',
                                                    spaces='drive').execute()
        else:
            response = drive_service().files().list(q="mimeType = 'application/vnd.google-apps.folder'",
                                                    corpora='domain',
                                                    spaces='drive',
                                                    pageToken=page_token).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['files']  # Drive api refers to files and folders as files.
        for folder in folders:
            if folder_id == folder["id"]:
                folder_data = folder
                getting_files = False

    return folder_data


def get_domain_folder_by_id_by_searching_files(folder_id):
    get_folder = drive_service().files().get(fileId=folder_id,
                                             fields='*',
                                             supportsAllDrives=True).execute()
    return get_folder


def get_domain_folder_by_id_by_searching_drive(drive_id):
    get_folder = drive_service().drives().get(driveId=drive_id,
                                              fields='*',
                                              useDomainAdminAccess=True).execute()
    return get_folder


def find_file_by_name(file_name: str) -> Union[bool, dict]:
    """
    Search through all the files that the Oauth user has access to. If the file_name is found it returns a dict of
    data about the file.

    Args:
        file_name: Name of the Google Drive file.

    Returns:
        bool, dict: If file_name is found it returns a dict. If the filde name is not found it returns False.

    """
    page_token = None
    getting_files = True
    file_data = False

    while getting_files:
        if not page_token:
            response = drive_service().files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                                    spaces='drive').execute()
        else:
            response = drive_service().files().list(q="mimeType != 'application/vnd.google-apps.folder'",
                                                    spaces='drive',
                                                    pageToken=page_token).execute()

        key_list = list(response.keys())
        if "nextPageToken" not in key_list:
            getting_files = False
        else:
            page_token = response["nextPageToken"]

        folders = response['files']
        for folder in folders:
            if file_name == folder["name"]:
                file_data = folder
                getting_files = False

    return file_data


def upload_csv_to_drive(csv_path: str, csv_name: str, folder_id: Optional[str] = None) -> str:
    """
    Upload csv files to Google Drive. If no folder_id is passed to the function then it will upload the csv
    to the users root of the G drive.

    Args:
        csv_path (str): Local path of the csv you wish to upload to google drive.
        csv_name (str): File name fo the local csv you wish to upload to google drive.
        folder_id (str): If you want to drop the file somewhere other than the root add the folder id.

    Returns:
        str: The google drive file id for the uploaded csv file.

    """
    if folder_id:
        csv_metadata = {'name': csv_name,
                        'parents': [folder_id]}
    else:
        csv_metadata = {'name': csv_name}

    csv_file = Path(f"{csv_path}/{csv_name}")
    media = MediaFileUpload(csv_file,
                            mimetype='text/csv')
    file = drive_service().files().create(body=csv_metadata,
                                          media_body=media,
                                          fields='id').execute()

    return file.get('id')


def create_folder_in_drive(folder_name: str, folder_id: Optional[str] = None) -> str:
    """
    This creates a folder in Google Drive. If no folder_id is passed to the function then folder will be created in the
    root of the G Drive.

    Args:
        folder_name (str): Name of the folder that is going to be created.
        folder_id (str): Google drive's folder id you will use to create the new folder in.
    Returns:
        str: Returns the google drive folder id of the newly created g drive folder.

    """
    if folder_id:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    folder = drive_service().files().create(body=file_metadata,
                                            fields='id').execute()

    return folder.get('id')


def create_file_in_drive(file_name: str, folder_id: Optional[str] = None) -> str:
    """
    This creates a file in Google Drive. If no folder_id is passed to the function then file will be created in the
    root of the G Drive.

    Args:
        file_name (str): Name of the file that is going to be created.
        folder_id (str): The Google drive's folder id you will use to create the new folder in.
    Returns:
        str: Returns the google drive file id of the newly created g drive file.

    """
    if folder_id:
        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': [folder_id]
        }
    else:
        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
    folder = drive_service().files().create(body=file_metadata,
                                            fields='id').execute()

    return folder.get('id')


def delete_file_or_folder(file_id: str) -> bool:
    """
    Permanently delete a file, skipping the trash.

    Args:
        file_id: ID of the file to delete.
    Returns:
        bool: If the file is deleted then it returns True. If its not deleted then it returns False.

    """
    # TODO Create unit test for this delete_file_or_folder
    try:
        drive_service().files().delete(fileId=file_id).execute()
        file_deleted_status = True

    except errors.HttpError:
        file_deleted_status = False

    return file_deleted_status


def empty_trash():
    """
    This will empty the Oauth user's trash bin.

    Returns:
        True: I have no way of testing this that i can think of so im just returning true. HACKY i know.
    """
    drive_service().files().emptyTrash().execute()

    return True


def create_sheets(title, values):
    spreadsheet = {
        'properties': {
            'title': title
        }
    }

    spreadsheet = sheets_service().spreadsheets().create(body=spreadsheet,
                                                         fields='spreadsheetId').execute()

    spreadsheet_id = spreadsheet.get('spreadsheetId')

    body = {
        'values': values
    }
    result = sheets_service().spreadsheets().values().update(spreadsheetId=spreadsheet_id,
                                                             range="A1",
                                                             valueInputOption="USER_ENTERED",
                                                             body=body).execute()

    return spreadsheet_id


def write_to_existing_sheet(sheet_id, values):
    body = {
        'values': values
    }
    result = sheets_service().spreadsheets().values().update(spreadsheetId=sheet_id,
                                                             range="A1",
                                                             valueInputOption="USER_ENTERED",
                                                             body=body).execute()

    return result



class ProjectEnvironment:
    """Create folders and files for project."""

    def __init__(self,
                 sheet_title: str,
                 project_folder_title: Optional[str] = None,
                 sub_folder_title: Optional[str] = None):
        """File and/folder names.

        :param sheet_title: Title for the Google sheets document.
        :type sheet_title: str
        :param project_folder_title: The name of the base folder for the project.
        :type project_folder_title: str
        :param sub_folder_title: The name of the folder that will be places inside the base folder.
        :type sub_folder_title: str
        """
        self.sub_folder_name = sub_folder_title
        self.sheet_title = sheet_title
        self.project_folder_name = project_folder_title

    def _project_folder_id(self):
        """Find folder_id if not create it.

        Search Google using Drive API v3 for a file/folder matching the project_folder_name parameter.

        If the file/folder is NOT found then a file/folder will be created and the id will be returned.

        Else if the file/folder is found then return its id.

        :return folder_id: The Google api identification number for a folder.
        """
        find_project_folder = find_my_folder_by_name_by_searching_files(self.project_folder_name)
        if not find_project_folder:
            folder_id = create_folder_in_drive(self.project_folder_name)

        else:
            folder_id = find_my_folder_by_name_by_searching_files(self.project_folder_name)
            folder_id = folder_id['id']

        return folder_id

    def _get_sub_folder_id(self, base_folder_id):
        """Find folder_id if not create it.

        Search Google using Drive API v3 for a file/folder matching the sub_folder_name parameter.

        If the file/folder is NOT found then a file/folder will be created and the id will be returned.

        Else if the file/folder is found then return its id.

        :param base_folder_id: Name of file/folder.
        :type base_folder_id: str
        :return: folder_id: The Google api identification number for a folder.
        """
        find_sub_folder = find_my_folder_by_name_by_searching_files(self.sub_folder_name)
        if not find_sub_folder:
            folder_id = create_folder_in_drive(self.sub_folder_name, base_folder_id)
        else:
            folder_id = find_my_folder_by_name_by_searching_files(self.sub_folder_name)['id']

        return folder_id

    def build(self):
        """Create the folder structure for project then create a Google sheets file.

        :return: folder_id: The Google api identification number for a folder.
        """
        if self.project_folder_name:
            folder_id = self._project_folder_id()
            if self.sub_folder_name:
                folder_id = self._get_sub_folder_id(folder_id)

        if folder_id:
            file_id = create_file_in_drive(self.sheet_title, folder_id)
        else:
            file_id = create_file_in_drive(self.sheet_title)

        return file_id