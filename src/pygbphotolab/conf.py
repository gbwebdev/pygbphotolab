import typing
from array import array
from os import path, makedirs
from os import name as osname
import logging

import yaml

class Conf:

    def __init__(self):
        if self._set_user_conffile():
            logging.info("Successfully set user conf file.")
        elif self._set_module_conffile():
            logging.info("Successfully set module conf file.")
        else:
            logging.error("No proper configuration file found.")
            exit(1)



    def _set_module_conffile(self) -> bool:
        script_filepath = path.realpath(__file__)
        script_dirpath = path.dirname(script_filepath)
        module_rootpath =  path.realpath(path.join(script_dirpath, "../.."))
        module_conffile_path = path.join(module_rootpath, "conf.yaml")

        if path.isfile(module_conffile_path):
            logging.info(f"Found a module-relative configuration file : {module_conffile_path}")
            if self._set_conffile(module_conffile_path):
                return True
        return False

    def _set_user_conffile(self) -> bool:
        if self.get_os() == "windows":
            return self._set_user_conffile_windows()
        else:
            return self._set_user_conffile_linux()
    
    def _set_user_conffile_windows(self) -> bool:
        homedir = path.expandvars('%USERPROFILE%')
        user_conffile_path = path.join(homedir, ".gbphotolab.conf.yaml")
 
        if path.isfile(user_conffile_path):
            logging.info(f"Found a user-relative configuration file : {user_conffile_path}")
            if self._set_conffile(user_conffile_path):
                return True
        return False

    def _set_user_conffile_windows(self) -> bool:
        homedir = path.expandvars('$HOME')
        user_conffile_path = path.join(homedir, ".gbphotolab.conf.yaml")
 
        if path.isfile(user_conffile_path):
            logging.info(f"Found a user-relative configuration file : {user_conffile_path}")
            if self._set_conffile(user_conffile_path):
                return True
        return False
    
    def _set_conffile(self, conffile_path) -> bool:
        conf_file = open(conffile_path, 'r')
        try:
            self._conf_file_content = yaml.safe_load(conf_file)
        except:
            logging.warning(f"Could not parse {conffile_path} as proper yaml")
            return False
        return True

    def get_os(self) -> str:
        if osname == "nt":
            return "windows"
        else:
            return "linux"

    def get_photolab_path(self, create_if_not_exists = False) -> path:
        try:
            res = self._conf_file_content['local']['photolab_path'] or "UNKNOWN"
        except KeyError:
            logging.error("local.photolab_path not found in the configuration file.")
            exit(1)
        
        if not path.isdir(res):
            if create_if_not_exists:
                makedirs(res)
            else:
                logging.error(f"{res} is not a directory.")
                exit(1)
        return res
        

    def get_camera_drive(self) -> path:
        try:
            res = self._conf_file_content['camera']['drive'] or "UNKNOWN"
        except KeyError:
            logging.error("camera.drive not found in the configuration file.")
            exit(1)
        
        if not path.isdir(res):
            logging.error(f"{res} is not a directory. Please check that the camera is plugged-in and the the drive letter is properly configured.")
            exit(1)
        return res
    
    def get_raw_extensions(self) -> typing.List[str]:
        try:
            res = self._conf_file_content['camera']['raw_extensions'] or ["RAW"]
        except KeyError:
            logging.error("camera.raw_extensions not found in the configuration file.")
            exit(1)
        
        return [ item.strip('.') for item in res]

    def get_keep_after_download(self) -> bool:
        try:
            res = self._conf_file_content['camera']['keep_after_download'] or True
        except KeyError:
            logging.error("camera.keep_after_download not found in the configuration file.")
            exit(1)
        
        return res