# Python program to AI smart spider project
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import urllib.parse

RELAX_TIME = 50
memory = []

url_max = 0
url_id = 0
title =""
#This function gets html and text data from wikipedia
def getUrl():
    global memory
    url_max = 0
    url_id = 0
    root_url = ""
    url_spider_count = 0
    url_error_count = 0
    
    url_address = []
    urls_found = []
    urls_session_found = []
    global title 
    print("WELCOME TO smart-media-scrapper")      
    print("Simple Python program ")    
    print("Developped Doctor G. ") 
    print("Under the supervision of Memo Sim") 
    print("help: gfm.mail.72@gmail.com\n")
  
    print("LOADING MEMORY")
    print("PLEASE WAIT...")
    
    # open file with list of url
    url_address =  get_urls_from_file("urls.txt", url_address)

    relax(RELAX_TIME)
    
    print("STARTING mp4, mkv and m3u8 file search...")
        
    # loop thru array of urls
    for current_url in url_address:
        
        relax(RELAX_TIME)
        root_url = current_url
        
        print("NEW LOOP")
        print("GETTING URL : " + current_url)
        
        try:
            if current_url not in memory:
                # get html file
                res = requests.get(current_url)
                html_page = res.content
                memory.append(current_url)

                print("STARTING TEXT EXTRACTION PROCESS")
                # HTML content processing
                soup_spider = BeautifulSoup(html_page, 'html.parser')
                title = soup_spider.title
               
                for item in soup_spider.find_all('link'): 
                    # Extract the url from the html tag
                    try:
                        # Extract the url from the html tag
                        found_url = str(item.get('href'))
                        print("LINK EXTRACTION: " + found_url)

                        if found_url.find('/details/') == 0:
                            found = found_url.find("/details/")
                            size_of_string = len("/details/")
                            adjusted = found + size_of_string
                            found_url = "https://archive.org/details/" + found_url[adjusted:len(found_url)]
                      
                        
                        if found_url.find('//') == 0:
                            found_url_open = "http:" + found_url
                            found_url_secure = "https:" + found_url
                            check_media(found_url_open)  
                            check_media(found_url_secure)  
                        else:
                            print(found_url)
                            check_media(found_url)   
                            if found_url not in memory:
                                with open("./urls/urls.txt", "a") as file:    
                                    file.write(found_url + "\n")
                                    file.close()
                        
                    except:
                        print("ERROR IN SOUP LINK EXTRACTION")    
                    
                # link extraction
                for item in soup_spider.find_all('a'): 
                

                    # Extract the url from the html tag
                    found_url = str(item.get('href'))

                    if found_url.find('/details/') == 0:
                        found = found_url.find("/details/")
                        size_of_string = len("/details/")
                        adjusted = found + size_of_string
                        found_url = "https://archive.org/details/" + found_url[adjusted:len(found_url)]
                      

                    if found_url.find('//') == 0:
                        found_url = "http:" + found_url
                        
                    if found_url.find('./') == 0:
                        found_url = current_url + found_url
                    
                    if found_url.find('http') == 0:
                        if found_url not in memory:
                            with open("./urls/urls.txt", "a") as file:    
                                file.write(found_url + "\n")
                                file.close()
                                        
                                print(found_url)
                                check_media(found_url)   

                # link extraction
                for item in soup_spider.find_all(): 
                

                    # Extract the url from the html tag
                    found_url = str(item.get('href'))

                    if (found_url != None):

                        if found_url.find('/details/') == 0:
                            found = found_url.find("/details/")
                            size_of_string = len("/details/")
                            adjusted = found + size_of_string
                            found_url = "https://archive.org/details/" + found_url[adjusted:len(found_url)]
                      
                        if found_url.find('//') == 0:
                            found_url = "http:" + found_url
                            
                        if found_url.find('./') == 0:
                            found_url = current_url + found_url
                        
                        if found_url.find('http') == 0:
                            if found_url not in memory:
                                with open("./urls/urls.txt", "a") as file:    
                                    file.write(found_url + "\n")
                                    file.close()
                                            
                                    print(found_url)
                                    check_media(found_url)             
        except:
            print("requests Error in REQUEST IN getUrl()")   
            continue
    getUrl()



def check_media(url_extracted):
    if (url_extracted.find(".m3u")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mov")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mp3")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mkv")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".m3u8")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mpg")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mpeg")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".swf")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".3gp")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".m2ts")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".vob")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".h264")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".ts")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".webm")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mpv")>0):
        downloadFile(url_extracted)

#This function read the texte
def save_url_content(spider_doc_title, output, ext, save_path ):
    try:     
        # open file with list of url
        with open(str(save_path) + str(spider_doc_title) + str(ext), "w") as file:
            file.write(output)
            file.close()
    except:
        print("Error in save_url_content()")  

def downloadFile(AFileName):

    print("MEDIA FOUND")
    # extract file name from AFileName
    filename = AFileName.split("/")[-1] 

    # download image using GET
    rawImage = requests.get(AFileName, stream=True)

              # Dump invalid urls
    with open("ARCHIVE.M3U", "a") as file:    
        global title
        
        print("FILM Mp4")
        print(AFileName)
        EXTINF_text = "#EXTINF:-1 group-title=\"" + str(filename) + "\""
        file.write(EXTINF_text + "\n")
        file.write(AFileName + "\n")
        file.close()      

    # save the image recieved into the file
    with open("./media/" + filename, 'wb') as fd:
        for chunk in rawImage.iter_content(chunk_size=1024):
            fd.write(chunk)
    return 

#This function cleans the document title
def clean_title(title):
    # Get spidered document title
    title = str(title)
    # add url decoder
    title = urllib.parse.unquote(title)
    
    # clean problematic char from title string
    title = title.replace("https://en.wikipedia.org", "")
    title = title.replace("/wiki/", "")
    title = title.replace("/","-")
    title = title.replace("/","-")
    title = title.replace("\\","-")
    title = title.replace("\"","")
    title = title.replace("\'","")
    title = title.replace("*", "-Asterix")

    # final string cleansing
    title = title.strip()
    title = title.lstrip()

    return title


# url file loading and cleaning process
def get_urls_from_file(list_name, url_address):

    print("Starting loading urls")
    print("with file name: " + list_name)
    relax(RELAX_TIME) 

    counter = 0
    i = 0

    # open file with list of url
    with open("./urls/" + list_name, "r") as file: 
        # reading each line     
        for url in file: 
            
            # Clean the url string
            url = endode_url(url)
            counter = counter + 1
                 
            # inset in url list object 
            url_address.append(url)

            if (counter>10000):
                counter = 0
                i= i +1
                print("Urls loaded : " + str(i*10000))
    
        file.close()

    return url_address

# This function cleans urls liste from doubles and visited links
def clean_urls_list(list_name):

    print("Starting clean_urls_list")
    counter = 0
    i = 0

    url_address = []
    url_address = get_urls_from_file(list_name, url_address)

    #url_address_visited = []
    #url_address_visited = get_urls_from_file(list_of_visited_links, url_address_visited)

    # Delete old dictionnary file
    with open(list_name, "w") as file:
        for url in url_address:           
            # Clean the url string
            url = endode_url(url)
            # inset in url list object if not double
            url_address = remove_url_double(url, url_address)
            
            #if not url in url_address_visited:
            file.write(url + "\n")
        
            if (counter>10000):
                counter = 0
                i= i +1
                print("Urls loaded : " + str(i*10000))     

        file.close()

def remove_url_double(list, item):

    for url in list:
        if (url==item):
            list.remove(url)
            print("Urls double found in list : " + url)
    return list
    
# This function cleans urls liste from doubles and visited links
def endode_url(url):
    # Clean the url string
    url = str(url.strip())
    return url

def download_youtube():
    # Download the Pluralsight 'we are one' video
    # url of video 
    url = "https://www.youtube.com/watch?v=TgRwoBgPM0o"
    # create video object
    video = pafy.new(url)
    # extract information about best resolution video available 
    bestResolutionVideo = video.getbest()
    # download the video
    bestResolutionVideo.download() 

def relax(s):
    time.sleep(s)

# url file loading and cleaning process
# clean_urls_list("urls.txt")

# start the url extraction
# start the html extraction
getUrl()