# -*- coding: utf-8 -*- 
 
import os
 
def file_name(file_dir): 
    for root, dirs, files in os.walk(file_dir):
        #print(root) #当前目录路径
        #print(dirs) #当前路径下所有子目录
        #print(files) #当前路径下所有非目录子文件
        for name in files:
            handle_jar(name)

def handle_jar(name):
    name = str(name).replace(".jar","")
    index = str(name).rindex("-")
    artifactId = name[0:index]
    version = name[index+1:len(name)]
    print("|"+name+"|"+artifactId +"|" + version+"|")

file_name("/Users/sloong/Downloads/BOOT-INF/lib")