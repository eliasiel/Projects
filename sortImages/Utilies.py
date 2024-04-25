
import glob
import pathlib
from collections import OrderedDict
import os
import shutil

class Utilies(object):

    @staticmethod
    def get_imgs(path,extention):
        imgs =[]
        main_path =glob.glob(path+'/*')
        for f in main_path:
            for e in extention:
                if e in f:
                    imgs.append(f)
        return imgs
    
    @staticmethod
    def get_dirs(path,extention):
        path = pathlib.Path(path)
        dirs = dict()
        for item in path.iterdir():
            if item.is_dir():
                path = item._str
                imgs =Utilies.get_imgs(path,extention)
                if len(imgs)== 0:
                    continue
                else:
                    dirs[os.path.basename(path)]=(imgs[0])
        try:
            dirs  = OrderedDict((key, dirs[key]) for key in sorted(dirs.keys(), key=int))
        except Exception as e:
            print ('Cant Order Folders')
            pass
        return dirs
    
    @staticmethod
    def add_new_dir(path):
        # Get a list of all folders in the base path
        folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
        for i, num in enumerate(folders):
            folders[i]= int(num)

        # Find the next available number
        next_number = 1 if not folders else max(folders) + 1

        # Create a new folder with the next number
        new_folder_path = os.path.join(path, str(next_number))
        os.makedirs(new_folder_path)
        return new_folder_path
    
    @staticmethod
    def copy_file(src,dest):
        shutil.move(src, dest)