from pathlib import Path
import os
import drive_tools


def test_drive_create_upload_delete():
    """
    This tests the functionality of finding, creating, and deleting folders. It also test uploading of a csv file to
    G drive.

    """
    # Empty the trash before you begin.
    drive_tools.empty_trash()

    tmp_base_folder = "delete_this_root_folder"

    # Confirm folder does not exist, if it does then delete it.
    find_folder = drive_tools.find_my_folder_by_name(tmp_base_folder)  # Find a folder that the Oauth user has access to.
    while find_folder:
        # Delete file
        drive_tools.delete_file_or_folder(find_folder['id'])
        # Try to find file again.
        re_try_find_folder = drive_tools.find_my_folder_by_name(tmp_base_folder)
        # If the file was deleted then stop the loop and move on
        if not re_try_find_folder:
            find_folder = False

    assert not find_folder

    # create base folder for test
    folder_id = drive_tools.create_folder_in_drive("delete_this_root_folder")
    assert isinstance(folder_id, str)

    # Confirm folder was created.
    find_folder = drive_tools.find_my_folder_by_name(tmp_base_folder)
    assert isinstance(find_folder, dict)

    """
    THIS IS A BIT HACKY. Sorry about that.
    
    HERE IS THE REASON FOR THE IF STATEMENT BELOW THIS COMMENT.
    
    When i test g_directory as a submodule it cant see the path to "tests_g_directory/func/test_upload_files".
    The reason is the working directory is off by a folder when running as a submodule. So the logic
    here is, if PYTHONPATH can see the "g_directory/" then im assuming that its being tested as a submodule.
    So i pass "g_directory/tests_g_directory/func/test_upload_files" as the "path_to_upload_csv" file path.
    
    
    """
    path_to_upload_csv = "tests/func/test_upload_files"

    # Upload csv file to folder_id in g drive.
    csv_file_name = "csv_move_to_drive_test.csv"
    upload_file = drive_tools.upload_csv_to_drive(csv_path=path_to_upload_csv,
                                                  csv_name=csv_file_name,
                                                  folder_id=folder_id)

    # Confirm file was uploaded.
    find_file = drive_tools.find_file_by_name(csv_file_name)
    assert isinstance(find_file, dict)


    # Delete folder and empty trash
    file_deleted = drive_tools.delete_file_or_folder(folder_id)
    assert file_deleted
    drive_tools.empty_trash()

    # Confirm file was deleted.
    find_folder = drive_tools.find_my_folder_by_name(tmp_base_folder)  # Find a folder that the Oauth user has access to.
    assert not find_folder






