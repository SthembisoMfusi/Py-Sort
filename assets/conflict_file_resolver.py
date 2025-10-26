
from hashlib import md5
import os
from os import path
import datetime
from pathlib import Path

def time_parser(tim:float):
   return datetime.datetime.fromtimestamp(tim)


def getInfo(file):
    return f''' 
    name    :  {file}
    Created :  {time_parser(path.getctime(file))}
    Modified:  {time_parser(path.getmtime(file))}
    Size    :  {path.getsize(file)}
    '''

def multi_reader(file1,file2,mode="rb"):
    with open(file1,mode) as file_desc1:
        file1_data=file_desc1.read()
    with open(file2,mode) as file_desc2:
        file2_data = file_desc2.read()
    return (file1_data,file2_data)


def is_same_file(file1,file2:Path):
    if md5(file1.split("/")[-1].encode()).hexdigest() == md5(file2.name.encode()).hexdigest():
        return True
    file1_data,file2_data = multi_reader(file1,file2)
    return md5(file1_data).hexdigest() == md5(file2_data).hexdigest()


def overwrite(file1,file2:Path):
    f1_data,f2_data=multi_reader(str(file1),str(file2))
   
    with open(str(file1),"wb") as out_file:
        out_file.write(f2_data)

    file2.unlink()
    



def rename(file,new_name=None):
    if not new_name:
        new_name=f"{"".join(str(file).split(".")[:-1])} Copy.{str(file).split(".")[-1]}"
    return Path.rename(file,new_name)
    
   
     


if __name__=="__main__":
    print(getInfo("hello.txt"))