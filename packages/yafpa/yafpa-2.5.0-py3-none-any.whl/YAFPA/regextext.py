import glob
from pathlib import Path
import os

BASEDIR = Path('D:/Users/Lili/Documents/GitHub/Owlly-house')
all_file = {}
post = []
folder = "_notes"
important_folder = ["_includes", "_layout", "_site"]
contents = glob.glob(f'{BASEDIR}/_*/**')
contents.extend(glob.glob(f'{BASEDIR}/_*/.*'))
print(contents)
for file in contents:
    print(os.path.basename(Path(file).parent))
    if not (any(i in file for i in important_folder)):
        print(os.path.basename(Path(file).parent.absolute()))
        if folder == os.path.basename(Path(file).parent.absolute()):
            post.append(file)
        else:
            print(post)
            folder = os.path.basename(Path(file).parent.absolute())
        all_file[folder] = post
print(all_file.keys())