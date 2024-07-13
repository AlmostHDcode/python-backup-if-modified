# python-backup-if-modified

### backup structure
source to backup 1: /path/to/my-project-1\
source to backup 2: /path/to/my-project-1

backup directory: /path/to/projects-backup

- resulting backup directory structure
  - projects-backup
    - my-project-1
      - 2024-01-01
      - 2024-01-02
      - etc...
    - my-project-2
      - 2024-01-02
      - etc...

### Conditions
* if backup directory is empty, or folder that makes the name of source does not exist in the backup directory
  * new backup is created

* if previous backups of your source dir do exist
  * Find which folder is the most recent, check if files in the source dir have been modified since the most recent backup
  * If modifications are found then a new backup is made

 * max number of backups to keep can be modified in the delete_old_backups function, or this function can be commented out if you don't want any backup to be deleted
 * example: if max number of backups is set to 10, then all of the oldest backups will be deleted until only the most recent 10 remain

# usage
source_dir1 = "/path/to/source/dir1"\
source_dir2 = "/path/to/source/dir2"\
source_dir3 = "/path/to/source/dir3"\
backup_dir = "/path/to/backup/dir"

backup_if_modified(source_dir1, backup_dir)\
delete_old_backups(source_dir1, backup_dir)

backup_if_modified(source_dir2, backup_dir)\
delete_old_backups(source_dir2, backup_dir)

backup_if_modified(source_dir3, backup_dir)\
delete_old_backups(source_dir3, backup_dir)
