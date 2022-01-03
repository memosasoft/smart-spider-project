#!/usr/bin/env python
from bs4 import BeautifulSoup

## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import datetime
import time
import mimetypes
import os
import urllib.parse  

urls_buffer = []
urls_links  = []

images_links = []
visited_links = []
urls_session  = []
images_session = []

loops = 0
max_loops = 100

def start_smart_spider():
    print("WELCOME MY SMART SPIDER") 
    print("------------------------------------")
    print("Loading memory lists...")
    
    # Load spider url memory 
    get_urls("urls_visited.txt", visited_links)
    get_urls("urls_images.txt", images_session)
    get_urls("urls_extracted.txt", urls_session)
    get_urls("urls.txt", urls_buffer)

    print("Loading memory lists completed...")
    print("Starting spider in 10 seconds...")
    
    relax(10)
    
    for url in urls_buffer:
        
        # download url
        html_file = get(url)
        
        if (html_file == None):
            continue
        
        print("Download success all seams to be working up to here...")
        print(url)
        relax(2)
        print("Continuing spider process...")
                
        save_html(url, html_file)
        print("Url saved to backup directory")
        relax(2)
        
        # add link to the visited list 
        # to avoid redownloading the url
        visited_links.append(url)
        print("Url added to visited links memory list")    
        relax(2)   
               
        # download full site and folder structure
        print("Starting full site download...")    
        full_download(url, html_file)    
        relax(2)
        
        # extract url
        urls_links = extract(url, html_file, "a", "href")
        
        if (urls_links == None):
            continue
        
        print("url links extraction completed and successful...") 
        relax(2)        
        
        # insert in session eliminating duplicate links
        for found_url in urls_links:
            if not found_url in urls_session:
                if not found_url in visited_links:
                    urls_session.append(found_url)

        # extract image
        images_links = extract(url, html_file, "img", "src") 
        
        if (images_links == None):
            continue
        
        print("images links extraction completed and successful...") 
        relax(2)  
          
        # insert in session eliminating duplicate links
        for img in images_links:
            if not img in images_session:
                images_session.append(img)
                get_image(img)
                #get_image_full_structure(url, img)
                
    # global cleanup to eliminate 
    # #links that have been visited
    cleanup()
    
    global loops
    global max_loops
    
    # Recursive function will never stop
    if (loops<max_loops):
        start_smart_spider()
    loops =+ 1

def cleanup():       
    
    print("Starting cleaning process... ")
    
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
                    
    print("Cleaning process completed... ")
                
    save_urls(urls_session, "urls.txt")
    
def get_urls(filename, urls_list):
    
    # read url file 
    with open(filename, "r", encoding="utf-8") as file:
        while True:
            line = file.readline()
            if not line:
                break
            
            line = line.strip()
            line = line.lstrip()
            
            if not line in urls_list:
                if (line.find("http")==0):
                    urls_list.append(line)
                    print("Loading url: " + line)
                else:
                    print("Junk in url this url will be ignored:" + line)
            
    file.close()

    # debug - function information        
    return urls_list
   
def get(url):
    try:  
        # Getting the webpage, creating a Response object.
        response = requests.get(url)
        
        # Print response encoding
        print ("This is the response encoding: " + response.encoding)
        print ("Downloading: " + url)
        
        # Extracting the source code of the page.
        html_file = response.text
        
        # Save to working buffer for analysis
        with open("buffer.php", "w", encoding="utf-8") as file:
            file.write(html_file)
            file.close()
            
        print ("Download success in get(url) no errors encountered :-) ")
        print ("Buffer filed created ./buffer.php")
        return html_file
    except:
        print('MAJOR EXCEPTION - getUrl()')    
        return None

def relax(sec):
    time.sleep(sec) 

def get_image(url):
    
    relax(5)  

    file_name = ""
    the_path = ""
    file_name_original = ""
    
    try:   
                   
        # Does the file have am extension
        # file name creating with timestamp
        file_name = datetime.datetime.now()
        file_name = file_name.strftime("img-%Y%M%H%S%f")

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream = True)
        ext = get_extension(r)
        file_name = file_name + "." + ext

        url_decoded = urllib.parse.unquote(url)
        file_name_original = get_url_file_name(url_decoded)
        print('This is the image file name before processing: ')
        print('Name: ' + file_name_original)
        
        file_name = file_name.split(":")[-1]   
        file_name_original = file_name_original.split(":")[-1]   
        
        print('This is the image file name after processing: ') 
        print('Name: ' + file_name_original)
        
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            
            # create the folder for the image
            the_path = create_directory(url_decoded)
           
            # Open a local file with wb ( write binary ) permission.
            with open("./images/" + file_name,'wb') as f:
                shutil.copyfileobj(r.raw, f)
                print('Success with : ' + file_name)
                relax(5)
                print('Preparing path and file for transfer of image : ')
                print('From :' + "./images/" + file_name)
                print('to :' + str(the_path) + file_name_original)
                relax(20)
                shutil.copyfile("./images/" + file_name, str(the_path) + file_name_original)
                print('Success with : ' + file_name_original)
                f.close()       
            
            print('Url in html: ' + url)     
              
            # Because image was downloaded add it to visited links

            visited_links.append(url)
        else:
            print('Image Couldn\'t be retreived')
            print('Image: ' + file_name_original)
            print('Path: ' + the_path)  
            print('Url in html: ' + url)    
    except:
        print('MAJOR EXCEPTION - Image Couldn\'t be retreived') 
        print('Image: ' + file_name_original)
        print('Url in html: ' + url)          

def clean_invalid_char(item):       
    #< (less than)
    #> (greater than)
    #: (colon)
    #" (double quote)
    #| (vertical bar or pipe)
    #* (asterisk)
    
    # clean path of invalid characters
    item = item.replace(":","+")    
    item = item.replace("|","+")
    item = item.replace("*","+")
    
    return item
       
def create_directory(url): 
    # create the folder for the image 
    url_decoded = urllib.parse.unquote(url) 
        
    print("Path cleaned from invalid characters..." )
                 
    file_name = get_url_file_name(url_decoded)
    file_folder = get_url_folder(url_decoded, file_name)
    site_name = get_site_name(url_decoded)

    path = "./data/" + site_name + file_folder
    path = clean_invalid_char(path)
      
    try:
        if not os.path.isdir(path):
            
            os.makedirs(path)
            #print ("Successfully created the directory %s " % path)
        else:
            print ("Directory allready exists %s " % path)   
            
        if file_name.find(".")<0:
            file_name = file_name + ".html"  
        
        print("Path to be created: " + path)
  
        return path
    
    except OSError:
        print("ERROR in create_directory(url)")
        print("")
        print("Creation of the directory %s failed" % path)
        print("file name: " + file_name)
        print("folder: " + file_folder)
        print("site name: " + site_name)
        
def save_html(url, html_file):     
    try:
        # Does the file have am extension
        # file name creating with timestamp
        file_name = datetime.datetime.now()
        file_name = file_name.strftime("web-%Y%M%H%S%f.html")
        
        # Save url info and text data
        file_name_data = file_name.replace("web", "data")
        file_name_data = file_name.replace("html", "txt")
        
        # Save html web page
        save_html_file("./html/", file_name, html_file)
        
        html_text = get_text(html_file)
        # Save html text and url info
        save_html_file("./html/", file_name_data, html_text)

        print("Good news...")    
        print("Non errors in save_html(url, html_file)")
        print("File " + file_name + " created")
        print("File " + file_name_data + " created")
        print("Files created for this url: " + url)
    except:
        print('MAJOR EXCEPTION - getUrl()')    
    return None

def full_download(url, html_file): 
    
    file_name = ""
    file_folder = ""
    site_name = ""
    
    try:
        ## Set up the image URL and filename
        # create the folder for the image 
        url_decoded = urllib.parse.unquote(url)   
               
        file_name = get_url_file_name(url_decoded)
        file_folder = get_url_folder(url_decoded, file_name)
        site_name = get_site_name(url_decoded)
        
        path = "./data/" + site_name + file_folder
        path = clean_invalid_char(path)  
        #print("Path to be created: " + path)
        
        try:
            
            if not os.path.isdir(path):
                os.makedirs(path)
                #print ("Successfully created the directory %s " % path)
            
            if file_name.find(".")<0:
                file_name = file_name + ".html"
                
            file_name = file_name.split(":")[-1]  
            
            html_file_decoded = clean_invalid_char(html_file)   
            save_html_file(path, file_name, html_file_decoded)
            
        except OSError:
            print ("Creation of the directory %s failed" % path)
    except:
        print("ERROR in full_download(url, html_file)")
        print("")
        print ("File name found: " + file_name)
        print ("Folder name found: " + file_folder)
        print ("Site name found: " + site_name )
        print ("Error building site structure in")
        print ("full_download(url, html_file)")

def save_html_file(folder, file_name, html_file):   
    try:     
        # Save to working buffer for analysis
        with open(folder + file_name, "w", encoding="utf-8") as file:
            file.write(html_file)
            file.close()
    except:
        print ("File name found: " + file_name)
        print ("Folder name found: " + folder)
        print ("Error in")
        print ("save_html_file(folder, file_name, html_file)")
        
def file_folder(url):
    try: 
        file_name = get_url_file_name(url)
        folder_found = get_url_folder(url, file_name)
        return folder_found
    except:
        print ("Error in")
        print ("file_folder(url)")
        print ("with: " + url) 
        
        return None      
        
def get_site_name(url):
    site_name = get_path(url)
    if (site_name.find("https://")>=0):
        site_name = site_name.replace("https://","")        
    if (site_name.find("http://")>=0):
        site_name = site_name.replace("http://","") 
    return site_name  
       
def get_url_file_name(url):  
    file_name = url.split("/")[-1]
    return file_name

def get_url_folder(url, file_name):  
    
    root_path = ""
    
    if ((url.find("http"))>=0):
        root_path = get_path(url)
    else:
        folder_name = url.replace(file_name)
        return folder_name
    
    folder_name = url.replace(file_name,"")
    folder_name = folder_name.replace(root_path,"")
    
    return folder_name

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

def debug_info(file_name, info): 
    # read url file
    with open(file_name, "r", encoding="utf-8") as file:
        file.write(info)
        file.close()
    
def extract(url, html, tag, sub_tag): 
    try:
        links = []
        
        soup = BeautifulSoup(html, "html.parser")
        
        for link in soup.find_all(tag):
            #print(link)
            link = link.get(sub_tag)
            
            # Debug exception - url parsing problem
            if link is None:
                continue
            if (link.find("javascript")>=0):
                continue
            if (link.find("#")>=0):
                continue
            if (len(link)<5):
                continue
            
            if not link is None:
                if link.find("http")==0:
                    link = link
                elif link.find("//")==0: 
                    protocol = get_protocol(url)   
                    link = protocol + link 
                else:
                    # get root https path
                    root_path = get_path(url)
                    if link[0] == "/":
                        link = root_path + link
                    else:
                        link = root_path + "/" + link
      
            #print("This is the link found : " + link)                  
            if not url in links:
                if not link is None:
                    if (link != url):
                        links.append(link)
                        #print("Link as been added to the link list: " + link)
        return links
    except:
        print("MAJOR EXCEPTION - extract()")
        print("With url: ") + url
        print("With tag: ") + tag
        print("With subtag: ") + sub_tag
        
        return None

def save_urls(urls, file_name): 
    # write url in visited site file
    with open(file_name, "w", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                file.write(url + "\n") 
        file.close()
    
def get_path(url): 
    
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

def get_protocol(url): 
    
    if (url.find("https://")>=0):  
        return "https:"
    
    if (url.find("http://")>=0):
        return "http:"
    
    # Just a guess
    return "https:"
          
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
start_smart_spider()