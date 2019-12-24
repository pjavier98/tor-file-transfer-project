import os

baseDir = 'files/'
dirName = input()

try:
    # Create target Directory
    dirName = baseDir + 'user_' + dirName 
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")