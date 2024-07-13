import os
import shutil
from datetime import datetime


def is_dir_empty(backup_dir):
    """
    Checks if a directory exists and if it is empty

    :param backup_dir: The directory to check
    :return: True or False
    """
    if os.path.isdir(backup_dir):  # Check if backup_dir exists
        if not os.listdir(backup_dir):  # Check if backup_dir is empty
            return True
        else:
            return False


def find_closest_backup(source_dir, backup_dir):
    """
    Finds the most recent backup
    backup_dir is assumed to have folders named after dates in y-m-d format

    :param source_dir: the source directory
    :param backup_dir: the backup directory
    :return closest folder: name of folder of most recent bakup date or False if none exist
    """
    source_name = os.path.basename(source_dir)
    closest_folder = None
    backup_folder_names = []

    for fname in os.listdir(os.path.join(backup_dir, source_name)):
        backup_folder_names.append(fname)

    if len(backup_folder_names) > 0:
        backup_folder_names.sort(reverse=True, key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        closest_folder = backup_folder_names[0]

    if closest_folder:
        return closest_folder
    else:
        return False


def check_files_modified(source_dir, backup_dir, closest_backup):
    """
    Checks if files in source_dir have been modified since closest backup

    :param source_dir: the source directory
    :param backup_dir: the backup directory
    :param closest_backup: most recent backup folder date
    :return files_modified: True or False
    """
    source_name = os.path.basename(source_dir)
    files_modified = False

    if closest_backup:
        # print(closest_backup)
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_dir)
                dest_path = os.path.join(backup_dir, source_name, closest_backup, rel_path)
                # print(src_path + " | " + dest_path)
                if os.path.exists(dest_path):  # if the corresponding file in src exists in the dest
                    src_mtime = os.path.getmtime(src_path)
                    dest_mtime = os.path.getmtime(dest_path)
                    if src_mtime > dest_mtime:
                        files_modified = True
                        break
                else:  # if the file exists in src but not in dest, then it is a new file not backed up yet, set modified to true
                    files_modified = True
                    break
    # print(files_modified)
    return files_modified


def backup_if_modified(source_dir, backup_dir):
    """
    Overall Function to backup files
    calls the other helper functions is_dir_empty, find_closest_backup, check_files_modified

    :param source_dir: the source directory
    :param backup_dir: the backup directory
    """
    source_name = os.path.basename(source_dir)
    current_date = datetime.now().strftime('%Y-%m-%d')

    # if the backup dir is empty
    # or if backup dir not empty but backup dir does not have a subdir named after the source
    # or if source dir folder does exist in backup, but is empty
    # then create new backup
    if is_dir_empty(backup_dir) or not os.path.isdir(os.path.join(backup_dir, source_name)) or is_dir_empty(os.path.join(backup_dir, source_name)):
        shutil.copytree(source_dir, os.path.join(backup_dir, source_name, current_date))
    else: # else if source dir does exist in backup and is not empty, find the most recent date, check for modifications
        closest_backup = find_closest_backup(source_dir, backup_dir)
        if check_files_modified(source_dir, backup_dir, closest_backup):
            if os.path.isdir(os.path.join(backup_dir, source_name, current_date)):
                shutil.rmtree(os.path.join(backup_dir, source_name, current_date))
            shutil.copytree(source_dir, os.path.join(backup_dir, source_name, current_date))
            print(source_name + ' File Modifications Were Found, New Backup Created')
        else:
            print(source_name + ' Has Not Been Modified Since the Most Recent Backup on ' + closest_backup + ', Skipping...')


def delete_old_backups(source_dir, backup_dir):
    max_backups = 4
    source_name = os.path.basename(source_dir)
    bak_dirs = [folder for folder in os.listdir(os.path.join(backup_dir, source_name)) if os.path.isdir(os.path.join(backup_dir, source_name, folder))]
    bak_dirs.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
    # print(bak_dirs)

    if len(bak_dirs) > max_backups:
        bak_dirs_del = bak_dirs[:len(bak_dirs) - max_backups]
        # print(bak_dirs_del)
        for fname in bak_dirs_del:
            # print(os.path.join(backup_dir, source_name, fname))
            shutil.rmtree(os.path.join(backup_dir, source_name, fname))


if __name__ == '__main__':
    source_dir = "/path/to/source/dir"
    backup_dir = "/path/to/backup/dir"
    backup_if_modified(source_dir, backup_dir)
    delete_old_backups(source_dir, backup_dir)
