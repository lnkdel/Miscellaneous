import os
import shutil
# entries = os.scandir('download')
# entries = os.listdir('download')

new_path = 'c:/MySpace/other/myfile/'
base_path = 'c:/MySpace/other/Downloads/'
for entry in os.listdir(base_path):
    if os.path.isfile(os.path.join(base_path, entry)):
        print(entry)
    else:
        child_path = os.path.join(base_path, entry)
        for e in os.listdir(child_path):
            # print(e)
            file_path = os.path.join(os.path.join(base_path, entry), e)
            shutil.copy(file_path, os.path.join(new_path, e))