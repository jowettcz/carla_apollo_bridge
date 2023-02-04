import os
import shutil

apollo_v7_module = "./modules"
movex_module = "./movex_modules"

for curDir, dirs, files in os.walk(movex_module):
    targetdir = curDir.replace("movex_modules","modules")
    # for subdir in dirs:
    #     if subdir == "proto":            
    #         new_full_dir = os.path.join(newdir, subdir)
    #         if not os.path.exists(new_full_dir):
    #             os.makedirs(new_full_dir)
    for file in files:
        if file.endswith(".proto"):
            src_fpath = os.path.join(curDir, file)
            dest_fpath = os.path.join(targetdir, file)
            try:
                shutil.copy(src_fpath, dest_fpath)
            except IOError as io_err:
                os.makedirs(os.path.dirname(dest_fpath))
                shutil.copy(src_fpath, dest_fpath)
            print(src_fpath)

    
