import os
from pathlib import Path
import drive_tools


def test_dir_service():
    assert str(type(drive_tools.drive_service())) == "<class 'googleapiclient.discovery.Resource'>"


def test_list_my_folders_by_searching_files():
    list_of_folders = drive_tools.list_my_folders_by_searching_files()
    assert isinstance(list_of_folders, list)

    for folder in list_of_folders:
        assert isinstance(folder, dict)

        kind = folder['kind']
        assert kind == 'drive#file'

        folder_id = folder['id']
        assert isinstance(folder_id, str)

        folder_name = folder['name']
        assert isinstance(folder_name, str)

        folder_type = folder['mimeType']
        assert folder_type == 'application/vnd.google-apps.folder'


def test_list_domain_folders_by_searching_files():
    list_domain_folders = drive_tools.list_domain_folders_by_searching_files()
    assert isinstance(list_domain_folders, list)

    for folder in list_domain_folders:
        assert isinstance(folder, dict)

        kind = folder['kind']
        assert kind == 'drive#file'

        folder_id = folder['id']
        assert isinstance(folder_id, str)

        folder_name = folder['name']
        assert isinstance(folder_name, str)


def test_find_my_folder_by_name_by_searching_files():
    file_that_exists = os.environ["G_DRIVE_TEST_FOLDER"]
    folder = drive_tools.find_my_folder_by_name_by_searching_files(file_that_exists)
    assert isinstance(folder, dict)

    kind = folder['kind']
    assert kind == 'drive#file'

    folder_id = folder['id']
    assert isinstance(folder_id, str)

    folder_name = folder['name']
    assert isinstance(folder_name, str)

    folder_type = folder['mimeType']
    assert folder_type == 'application/vnd.google-apps.folder'


def test_find_domain_folder_by_name_by_searching_files():
    # TODO i don't own the domain folder so it is subject to change
    file_that_exists = os.environ["G_DRIVE_DOMAIN_TEST_FOLDER"]
    folder = drive_tools.find_domain_folder_by_name_by_searching_files(file_that_exists)
    assert isinstance(folder, dict)

    kind = folder['kind']
    assert kind == 'drive#file'

    folder_id = folder['id']
    assert isinstance(folder_id, str)

    folder_name = folder['name']
    assert isinstance(folder_name, str)

    folder_type = folder['mimeType']
    assert folder_type == 'application/vnd.google-apps.folder'




def test_find_domain_folder_by_id():
    file_id_that_exists = os.environ["G_DRIVE_TEST_FOLDER_ID"]
    folder = drive_tools.find_domain_folder_by_id(file_id_that_exists)
    assert isinstance(folder, dict)

    kind = folder['kind']
    assert kind == 'drive#file'

    folder_id = folder['id']
    assert isinstance(folder_id, str)

    folder_name = folder['name']
    assert isinstance(folder_name, str)

    folder_type = folder['mimeType']
    assert folder_type == 'application/vnd.google-apps.folder'


def test_find_file_by_name():
    file_name = "Don't delete me i use this for testing"
    find_file = drive_tools.find_file_by_name(file_name)
    assert isinstance(find_file, dict)


def test_upload_csv_to_drive():
    path_to_upload_csv = "tests/func/test_upload_files"

    csv_file_name = "csv_move_to_drive_test.csv"
    file_id = drive_tools.upload_csv_to_drive(csv_path=path_to_upload_csv, csv_name=csv_file_name)
    assert isinstance(file_id, str)

    # Find file to confirm it was created.
    find_file = drive_tools.find_file_by_name(csv_file_name)
    assert isinstance(find_file, dict)

    # delete file from G drive after testing it.
    delete_status = drive_tools.delete_file_or_folder(file_id)
    assert delete_status


def test_create_folder_in_drive():
    # Create a folder name for testing
    test_create_folder = "test_create_folder_del_me"

    # If test_create_folder exists then delete it before the test.
    find_test_folder_name = drive_tools.find_my_folder_by_name_by_searching_files(test_create_folder)
    # TODO this logic should live in the delete function itself
    # TODO create a pull request for adding this logic to the delete function
    if find_test_folder_name:
        file_found = True
        while file_found:
            find_test_folder_name = drive_tools.find_my_folder_by_name_by_searching_files(test_create_folder)
            if find_test_folder_name:
                drive_tools.delete_file_or_folder(find_test_folder_name['id'])
            else:
                file_found = False

    # Confirm test_create_folder does NOT exist.
    find_test_folder_name = drive_tools.find_my_folder_by_name_by_searching_files(test_create_folder)
    assert not find_test_folder_name

    # Create test_create_folder in g drive.
    creating_in_root = drive_tools.create_folder_in_drive(test_create_folder)
    assert isinstance(creating_in_root, str)

    # Confirm test_create_folder DOES exist.
    find_test_folder_name = drive_tools.find_my_folder_by_name_by_searching_files(test_create_folder)
    assert find_test_folder_name

    # Clean up test env.
    drive_tools.find_my_folder_by_name_by_searching_files(creating_in_root)

    # Confirm test_create_folder was removed.
    find_test_folder_name = drive_tools.find_my_folder_by_name_by_searching_files(test_create_folder)
    if find_test_folder_name:
        file_found = True
        while file_found:
            find_test_folder_name = drive_tools.find_my_folder_by_name_by_searching_files(test_create_folder)
            if find_test_folder_name:
                drive_tools.delete_file_or_folder(find_test_folder_name['id'])
            else:
                file_found = False

    assert not find_test_folder_name


def test_create_file_in_drive():
    # Create a file name for testing
    test_create_file = "test_create_file"

    # If test_create_file exists then delete it before the test.
    find_test_file_name = drive_tools.find_file_by_name(test_create_file)

    if find_test_file_name:
        file_found = True
        while file_found:
            find_test_file_name = drive_tools.find_file_by_name(test_create_file)
            if find_test_file_name:
                drive_tools.delete_file_or_folder(find_test_file_name['id'])
            else:
                file_found = False

    # Confirm test_create_folder does NOT exist.
    find_test_file_name = drive_tools.find_file_by_name(test_create_file)
    assert not find_test_file_name

    # Create test_create_file in g drive.
    creating_in_root = drive_tools.create_file_in_drive(test_create_file)
    assert isinstance(creating_in_root, str)

    # Confirm test_create_file DOES exist.
    find_test_file_name = drive_tools.find_file_by_name(test_create_file)
    assert find_test_file_name

    # Clean up test env.
    drive_tools.find_file_by_name(creating_in_root)

    # Confirm test_create_file was removed.
    find_test_file_name = drive_tools.find_file_by_name(test_create_file)
    if find_test_file_name:
        file_found = True
        while file_found:
            find_test_file_name = drive_tools.find_file_by_name(test_create_file)
            if find_test_file_name:
                drive_tools.delete_file_or_folder(find_test_file_name['id'])
            else:
                file_found = False

    assert not find_test_file_name


def test_delete_file_or_folder():
    file_name_to_delete = "del_this_file"

    # Create file
    file_id = drive_tools.create_file_in_drive(file_name_to_delete)
    # Confirm the file exists and get the file id
    found_file = drive_tools.find_file_by_name(file_name_to_delete)
    assert found_file
    # Delete file
    drive_tools.delete_file_or_folder(file_id)

    file_found = True
    while file_found:
        find_file = drive_tools.find_file_by_name(file_name_to_delete)
        if not find_file:
            file_found = False

    # Confirm you cant find the file after deleting it.
    assert not drive_tools.find_file_by_name(file_name_to_delete)






