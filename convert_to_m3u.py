#This function gets html and text data from wikipedia
# Import Module
import os
# Python program to AI smart spider project
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import urllib.parse

title =""

url_id = 0
url_max = 0

def read_file():
    
    # Folder Path
    path = "/home/linux/Bureau/Programmation/media-url-spider-1.0/media/"
    
    # Change the directory
    os.chdir(path)
    # iterate through all file
    for file in os.listdir():
        # call read text file function
        read_text_file(file, path)

def read_text_file(file, file_path):
    try:
        title, mp4 = extract_data_from_file(file) 
        write_to_m3u(title, mp4)
    except:
        pass

def extract_data_from_file(file):
    try:
        file_z = open(file, "r")
        data = file_z.read()
        print("STARTING TEXT EXTRACTION PROCESS")
    except:
        pass    
    try:
        # HTML content processing
        soup_spider = BeautifulSoup(str(data), 'html.parser')
            # Extract the url from the html tag
        title = soup_spider.find('meta', attrs={'property':'og:title'})
        video = soup_spider.find('meta', attrs={'property':'og:video'}) 
    except:
        pass    
    try:
        if ( video != None):
            t = title.get('content')
            v = video.get('content') 
            return t, v 
    except:
        return "", ""   
    # link extraction 
    
def write_to_m3u(title, mp4):
    with open("../ARCHIVE.M3U", "a") as file:
        file.write("#EXTINF:-1 " + title + "\n")
        file.write(mp4 + "\n")

def main():
    files = read_file()
main()