import argparse
import shutil
from datetime import datetime, timedelta
import os
import pandas as pd
from send2trash import send2trash

ignore_files = [".DS_Store"]
dry_run = False


def move_to_folder(src, dest):
    if not dry_run:
        shutil.move(src, dest)
    else:
        print(f"File ${src} to be archived")


def send_to_trash(file):
    if not dry_run:
        send2trash(file)
    else:
        print('File ' + file + " will be deleted")


def get_date(epoch):
    return datetime.fromtimestamp(epoch)


def get_file(file, f):
    size_mb = os.stat(f).st_size * 0.000001
    now = datetime.now()
    aage = now - get_date(os.stat(f).st_atime)
    mage = now - get_date(os.stat(f).st_mtime)
    access_after = get_date(os.stat(f).st_atime) - get_date(os.stat(f).st_mtime)
    in_frequent_access = access_after < timedelta(hours=1)
    access_percent = access_after.seconds / mage.seconds
    return {
        "file": file,
        "path": f,
        "ext": os.path.splitext(f)[1].lower(),
        "st_atime": get_date(os.stat(f).st_atime),
        "st_mtime": get_date(os.stat(f).st_mtime),
        "aage": aage,
        "mage": mage,
        "access_after": access_after,
        "in_frequent_access": in_frequent_access,
        "access_percent": access_percent,
        "size_mb": size_mb
    }


def eval(path, folder):
    print("What to do with path=", path)
    print("(D)elete or (A)rchive (S)kip (O)pen")
    i = input().lower()

    if i == 'd':
        send_to_trash(path)
    if i == "a":
        move_to_folder(path, folder)


def get_files(dir):
    files = [get_file(f, os.path.join(dir, f)) for f in os.listdir(dir)]
    df = pd.DataFrame(files)
    df = df[~df['file'].isin(ignore_files)]
    return df


def print_hi(dir):
    df = get_files(dir)
    is_old = df['aage'].dt.total_seconds() > 7 * 24 * 3600
    not_big_file = (df['size_mb'] < 500)
    is_installer = (df['ext'].isin(['.exe', '.dmg', '.pkg', '.app']))
    is_zip = (df['ext'].str.lower().isin(['.zip', '.archive']))
    is_quicken = (df['ext'].str.lower().isin(['.qif']))
    is_temp_document = (df['ext'].isin(['.html', '.txt']))
    is_document = df['ext'].isin(['.pdf', '.xlsx'])
    is_image = df['ext'].isin(['.jpg', '.jpeg', '.png'])
    data = df[
        is_old &
        is_installer &
        not_big_file
        ]
    zip_files = df[
        is_old & not_big_file & is_zip
        ]
    qif = df[is_old & not_big_file & is_quicken]
    temp_doc = df[is_old & is_temp_document]
    doc = df[is_old & is_document]
    image = df[is_old & is_image]
    old = df[is_old]
    auto_deleted_paths = list(data['path']) + list(zip_files['path']) + list(qif['path']) + list(temp_doc['path'])
    if len(auto_deleted_paths) > 0:
        print('Auto removal of the following files')
        print(auto_deleted_paths)
        print("(Y)es or (R)eview (S)kip")
        i = input().lower()
        if i == 'y':
            for path in auto_deleted_paths:
                send_to_trash(path)

    if len(list(doc["path"])):
        print("Reviewing ", len(list(doc["path"])), " docs")
        for path in list(doc["path"]):
            eval(path, "/Users/Work/Documents")

    if len(list(image["path"])):
        print("Reviewing ", len(list(image["path"])), " image")
        for path in list(image["path"]):
            eval(path, "/Users/Work/Documents")

    if len(list(old["path"])):
        print("Reviewing ", len(list(old["path"])), " old items")
        for path in list(old["path"]):
            eval(path, "/Users/Work/Documents")
    df_fresh = get_files(dir)
    print(f"Done!!! {len(df_fresh)} items left")
    print(df_fresh[['path', 'ext', 'aage']])
    print("Review more? No")
    i = input().lower()
    if i == "y":
        for path in list(df_fresh["path"]):
            eval(path, "/Users/Work/Documents")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Location to run")
    args = parser.parse_args()
    print_hi(args.path or "/Users/Work/Downloads")
