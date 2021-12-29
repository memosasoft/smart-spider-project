url_max = 0
url_id = 0
title =""
#This function gets html and text data from wikipedia
# Import Module
import os
# Python program to AI smart spider project
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import urllib.parse

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
    title, mp4  = extract_data_from_file(file)
    write_to_m3u(title, mp4)

def extract_data_from_file(file):
    file_z = open(file)
    data = file_z.read()
    print("STARTING TEXT EXTRACTION PROCESS")
    print(data)
  
    # HTML content processing
    soup_spider = BeautifulSoup(str(data), 'html.parser')
           # Extract the url from the html tag
    title = soup_spider.find("og:title").content
    video = soup_spider.find("og:video").content

    # link extraction
    return title, video   
    
def write_to_m3u(title, mp4):
    if (title!= None):
        with open("archive.m3u", "a", encoding="utf-8") as file:
            file.write("#EXTINF:-1 " + title + "\n")
            file.write(mp4 + "\n")

def main():
    files = read_file()
main()