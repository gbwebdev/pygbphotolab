#!/usr/bin/env python3

from os import path, makedirs, remove
from datetime import date
from glob import glob
import logging
import shutil

from pygbphotolab import conf as module_conf

conf = module_conf.Conf()

dcim_path = path.join(
        conf.get_camera_drive(),
        "DCIM"
    )
incomming_path = path.join(
        conf.get_photolab_path(),
        "Incomming"
    )
incomming_raw_path = path.join(
        incomming_path,
        "RAW"
    )
incomming_jpeg_path = path.join(
        incomming_path,
        "JPEG"
    )
already_downloaded_path = path.join(
        conf.get_camera_drive(),
        "already_downloaded"
    )
already_downloaded_today_path = path.join(
        already_downloaded_path,
        str(date.today())
    )
keep_after_download = conf.get_keep_after_download()

if keep_after_download:
    makedirs(already_downloaded_today_path, exist_ok=True)

makedirs(incomming_raw_path, exist_ok=True)
makedirs(incomming_jpeg_path, exist_ok=True)

raws = []
for raw_ext in conf.get_raw_extensions():
    raws += glob(path.join(
                        path.join(dcim_path, "**"),
                        f"*.{raw_ext}"
                    ), recursive=True)

logging.info("Downloading RAW files...")
for raw in raws:
    dst = path.join(incomming_raw_path, path.basename(raw))
    if not path.isfile(dst):
        shutil.copy2(raw, dst)
    if keep_after_download:
        shutil.move(raw,already_downloaded_today_path)
    else:
        remove(raw)
logging.info("Done downloading RAW files.")


jpegs = []
for jpeg_ext in ['JPG', 'JPEG']:
    jpegs += glob(path.join(
                        path.join(dcim_path, "**"),
                        f"*.{jpeg_ext}"
                    ), recursive=True)

logging.info("Downloading JPEG files...")
for jpeg in jpegs:
    dst = path.join(incomming_jpeg_path, path.basename(jpeg))
    if not path.isfile(dst):
        shutil.copy2(jpeg, dst)
    if keep_after_download:
        shutil.move(jpeg,already_downloaded_today_path)
    else:
        remove(raw)
logging.info("Done downloading JPEG files.")


print(f"JPEGs have been dowloaded to \"{incomming_jpeg_path}\"")
print(f"RAWs have been dowloaded to \"{incomming_raw_path}\"")
if keep_after_download:
    print(f"Downloaded files were kept on the camera (but moved to \"{already_downloaded_today_path}\"")
else:
    print(f"Downloaded files were deleted from the camera.")

input("Done. Press a key to exit.")