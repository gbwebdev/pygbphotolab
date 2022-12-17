#!/usr/bin/env python3

from os import path, makedirs, remove
from datetime import date
from glob import glob
import logging
import shutil

def exec():
    from pygbphotolab import conf as module_conf

    conf = module_conf.Conf()

    selected_jpegs = []
    for jpeg_ext in ['JPG', 'JPEG']:
        selected_jpegs += glob(path.join(
                            conf.get_JPEG_selection_path(),
                            f"*.{jpeg_ext}"
                        ))

    for selected_jpeg in selected_jpegs:
        selected_jpeg_basename = path.splitext(path.basename(selected_jpeg))[0]
        corresponding_raws = glob(path.join(
                            conf.get_incomming_raw_path(),
                            f"{selected_jpeg_basename}.*"
                        ))
        if len(corresponding_raws) != 1:
            logging.warning("Abnormal number of corresponding RAWs found.")
            print(f"{selected_jpeg_basename}.*")
            print(corresponding_raws)
        else :
            corresponding_raw = corresponding_raws[0]
            shutil.move(corresponding_raw,conf.get_RAW_selection_path())

    remaining_raws = []
    for raw_ext in conf.get_raw_extensions():
        remaining_raws += glob(path.join(
                            conf.get_incomming_raw_path(),
                            f"*.{raw_ext}"
                        ))

    for remaining_raw in remaining_raws:
        remaining_raw_basename = path.splitext(path.basename(remaining_raw))[0]
        corresponding_jpegs = glob(path.join(
                            conf.get_incomming_jpeg_path(),
                            f"{remaining_raw_basename}.*"
                        ))
        if len(corresponding_jpegs) == 0:
            remove(remaining_raw)

if __name__ == "__main__":
    exec()