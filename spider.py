#!/usr/bin/env python
from bs4 import BeautifulSoup

## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import datetime
import time
import mimetypes
import _thread

urls_buffer = []
urls_links  = []

images_links = []
visited_links = []
urls_session  = []
images_session = []

def start_image_miner():
  
    # Load image-miner url memory 
    get_urls("urls_visited.txt", visited_links)
    get_urls("urls_images.txt", images_session)
    get_urls("urls_extracted.txt", urls_session)
    get_urls("urls.txt", urls_buffer)

    for url in urls_buffer:
        
        # download url
        html_file = get(url)
        
        if (html_file == None):
            continue
        
        visited_links.append(url)
        
        # extract url
        urls_links = extract(url, html_file, "a", "href")
        
        if (urls_links == None):
            continue
        
        # insert in session eliminating duplicate links
        for found_url in urls_links:
            if not found_url in urls_session:
                if not found_url in visited_links:
                    urls_session.append(found_url)

        # extract image
        images_links = extract(url, html_file, "img", "src")
        
        if (images_links == None):
            continue
        
        # insert in session eliminating duplicate links
        for img in images_links:
            if not img in images_session:
                images_session.append(img)
                get_image(img)
                
    # global cleanup to eliminate 
    # #links that have been visited
    cleanup()
        
    # Recursive function will never stop
    start_image_miner()

def cleanup():       
    # Save all visited urls
    save_urls(visited_links, "urls_visited.txt")
    save_urls(urls_session, "urls_extracted.txt")
    save_urls(images_session, "urls_images.txt")
    
    # create a clean list
    clean_list = []
    for cleanup in urls_session:
        if not cleanup in visited_links:
            clean_list.append(cleanup)
    
    # Empty session url list
    urls_session.clear()
    
    # Rebuild the session list and reclean
    for url in clean_list:
        if not url in urls_session:
            if not url in visited_links:
                urls_session.append(url)     
            
    save_urls(urls_session, "urls.txt")
    
def get_urls(filename, urls_list):
    
    # read url file 
    with open(filename) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            if not line.strip() in urls_list:
                urls_list.append(line.strip())
            
    fp.close()

    # debug - function information        
    return urls_list
   
def get(url):
    try:  
        # Getting the webpage, creating a Response object.
        response = requests.get(url)
    
        # Extracting the source code of the page.
        html_file = response.text
        
        with open("buffer.php", "w", encoding="utf-8") as file:
            file.write(html_file)
            file.close()

        return html_file
    except:
        print('MAJOR EXCEPTION - getUrl()')    
        return None

def relax(sec):
    time.sleep(sec) 

def get_image(url):
    
    relax(2)  

    try:        
        ## Set up the image URL and filename
        filename = url.split("/")[-1]
        
        # Does the file have am extension
        # file name creating with timestamp
        filename = datetime.datetime.now()
        filename = filename.strftime("img-%Y%M%H%S%f")

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream = True)
        ext = get_extension(r)
        filename = filename + "." + ext

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # Because image was downloaded add it to visited links
            visited_links.append(url)
            
            # Open a local file with wb ( write binary ) permission.
            with open("./images/" + filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                       
            print('Image successfully Downloaded: ',filename)
        else:
            print('Image Couldn\'t be retreived')
    except:
        print('MAJOR EXCEPTION - Image Couldn\'t be retreived')
        
def get_text(the_page):  
    soup = BeautifulSoup(the_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ""
    blacklist = [
        '[document]',
        'script',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'css',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def debug_info(info): 
    # read url file
    f = open("debug.txt", "a")
    f.write(info)
    f.close()
    
def extract(url, html, tag, sub_tag): 
    try:
        links = []
        
        soup = BeautifulSoup(html, "html.parser")
        
        for link in soup.find_all(tag):
            print(link)
            link = link.get(sub_tag)
            
            # Debug exception
            if link is None:
                continue
            if (link.find("javascript")>=0):
                continue
            if (link.find("#")>=0):
                continue
            if (len(link)<5):
                continue
            
            if not link is None:
                if link.find("http")<0:
                    # get root https path
                    root_path = get_path(url, link)
                    if link[0] == "/":
                        link = root_path + link
                    else:
                        link = root_path + "/" + link
            if not url in links:
                if (link != url):
                    links.append(link)
                    print(link)
            
        return links
    except:
        print('MAJOR EXCEPTION - extract()')
        return None

def save_urls(urls, file_name): 
    # write url in visited site file
    with open(file_name, "w", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                file.write(url + "\n") 
        file.close()
    
def get_path(url, link): 
    
    if (url.find("https://")>=0):
        url = url.replace("https://","")
        split_url = url.split("/")   
        return "https://" + split_url[0]
    
    if (url.find("http://")>=0):
        url = url.replace("http://","")   
        split_url = url.split("/")   
        return "http://" + split_url[0]
    
    # Just a guess
    url = url.replace("https://","")
    split_url = url.split("/")   
    return "https://" + split_url[0]
          
def get_extension(response):
    mtype = response.headers.get("Content-Type", "image/jpeg")
    mtype = mtype.partition(";")[0]

    if "/" not in mtype:
        mtype = "image/" + mtype

    if mtype in MIMETYPE_MAP:
        return MIMETYPE_MAP[mtype]

    exts = mimetypes.guess_all_extensions(mtype, strict=False)
    if exts:
        exts.sort()
        return exts[-1][1:]

    return "txt"

MIMETYPE_MAP = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/x-bmp": "bmp",
    "image/x-ms-bmp": "bmp",
    "image/webp": "webp",
    "image/svg+xml": "svg",

    "image/vnd.adobe.photoshop": "psd",
    "image/x-photoshop": "psd",
    "application/x-photoshop": "psd",

    "video/webm": "webm",
    "video/ogg": "ogg",
    "video/mp4": "mp4",

    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/webm": "webm",
    "audio/ogg": "ogg",
    "audio/mpeg": "mp3",

    "application/zip": "zip",
    "application/x-zip": "zip",
    "application/x-zip-compressed": "zip",
    "application/rar": "rar",
    "application/x-rar": "rar",
    "application/x-rar-compressed": "rar",
    "application/x-7z-compressed": "7z",

    "application/ogg": "ogg",
    "application/octet-stream": "bin",
}

# Start image spider/miner program
start_image_miner()