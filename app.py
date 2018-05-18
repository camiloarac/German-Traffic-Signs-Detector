import click
import requests
import os
import zipfile
from tqdm import tqdm
import math

@click.group()
def cli():
    pass

@cli.command()
def download():
    """This subcommand gets the dataset from a url, unzips it and organizes 
    the files by storing 80% of them in the train folder and the remaining
    20% in the test folder"""
    downloadURL = "http://benchmark.ini.rub.de/Dataset_GTSDB/FullIJCNN2013.zip"
    myFile = "FullIJCNN2013.zip"
    train_path = "train/"
    test_path = "test/"
    r = requests.get(downloadURL, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0)); 
    print(total_size)
    block_size = 1024
    wrote = 0 
    with open(myFile, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size), 
                         unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    createFolder(train_path)
    createFolder(test_path)
    myZipFile = zipfile.ZipFile(myFile)
    myDict = {}
    for name in myZipFile.namelist():
        nameStrings = name.split("/")
        if (len(nameStrings) > 2)  & (len(nameStrings[-1]) > 0):
            myDict[nameStrings[1]] = myDict.get(nameStrings[1], 0) + 1
    for elem in myDict:
        myDict[elem]=int(myDict[elem]*0.8)        
    for name in myZipFile.namelist():
        nameStrings = name.split("/")
        if (len(nameStrings) > 2)  & (len(nameStrings[-1]) > 0):
            if myDict[nameStrings[1]] > 0:
                with open("train/Folder"+ nameStrings[1] +"Image"+ nameStrings[2],  
                      "wb") as f:  # open the output path for writing
                    f.write(myZipFile.read(name))
                myDict[nameStrings[1]]-= 1
            else:
                with open("test/Folder"+ nameStrings[1] +"Image"+ nameStrings[2],  
                      "wb") as f:  # open the output path for writing
                    f.write(myZipFile.read(name))
    
def createFolder(folderPath):
    """Checks if the folder exists, if not it creates the folder"""
    directory = os.path.dirname(folderPath)
    if not os.path.exists(directory):
        os.makedirs(directory)
if __name__ == "__main__":
    cli()
