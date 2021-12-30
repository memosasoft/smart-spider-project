# Python program to AI smart spider project
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import urllib.parse

from fake_useragent import UserAgent

RELAX_TIME = 0.0000001
memory = []
ua = UserAgent()

#This function gets html and text data from wikipedia
def main():
    global memory
    url_spider_count = 0
    url_error_count = 0
    
    url_address = []
    urls_found = []
    urls_visited = []

    print("WELCOME TO media-spider")  
    print("help: gfm.mail.72@gmail.com\n")

    print("LOADING MEMORY")
    print("PLEASE WAIT...")
    
    # open file with list of url
    url_address =  get_urls_from_file("urls.txt", url_address)
    
    print("STARTING mp4, mkv and m3u8 file search...")
    memory = []

    # loop thru array of urls
    for current_url in url_address:
        
        # Is it the end of the liste
        if current_url == "" and len(url_address)<=0:
            break
        
        import requests as rq 
        from bs4 import BeautifulSoup as bs
        
        try:
            page = rq.get(current_url, headers={'User-Agent': ua.random},timeout=10)
            html = bs(page.text, 'lxml')

            hrefs = html.find_all("a")
            all_hrefs = []
            for href in hrefs:
                # print(href.get("href"))
                links = href.get("href")
                try:   
                    if not "http" in links:
                        links = fix_link(links, current_url)
                    
                    if links not in memory:               
                        url_address.append(links)
                        check_media(links)
                        print("EXtracted URL : " + links)
                        memory.append(links)
                except:
                    pass
            
            hrefs = html.find_all("link")
            all_hrefs = []
            for href in hrefs:
                # print(href.get("href"))
                links = href.get("href")
                try:
                    if not "http" in links:
                        links = fix_link(links, current_url)
                    
                    if links not in memory:               
                        url_address.append(links)
                        check_media(links)
                        print("EXtracted URL : " + links)
                        memory.append(links)
                except:
                    pass
        except:
            print("MAIN LOOP FAILURE")                
    # open file with list of url
    url_address =  get_urls_from_file("urls.txt", url_address)
    
    # Recursive function
    main()
        
def fix_link(url, current_url):
    
    if (url.find('//')==0):
        url = "https:" + url
    if (url.find('/')==0):
        url = current_url + url
    if (url.find('#')==0):
        url = current_url
    return url
        
def check_media(url_extracted):
    if (url_extracted.find(".m3u")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mov")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".mkv")>0):
        downloadFile(url_extracted)
    if (url_extracted.find(".avi")>0):
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
        
def downloadFile(url_extracted):
    
    print("MEDIA FOUND starting PROCESS")
    print("MEDIA FOUND : " + url_extracted)

    import uuid
    filename = str(uuid.uuid4())
    ext = url_extracted.split(".")[-1] 

    # Dump invalid urls
    # Request the profile picture of the OP:
    import wget
    wget.download(url_extracted, './media/' + filename +"."+ ext + " -q --show-progress --progress=dot")
  
    print("MEDIA FOUND SAVED")
    # extract file name from AFileName
    title = url_extracted.split("/")[-1] 
    
    from six.moves.html_parser import HTMLParser
    h = HTMLParser()
    
    print(h.unescape(title))
    title = h.unescape(title)
    title = clean_title(title)
    
    # Dump invalid urls
    with open("ARCHIVE.M3U", "a") as file:    
        print("FILM TROUVER")
        print(url_extracted)
        EXTINF_text = "#EXTINF:-1, group-title=\"" + title + "\""
        file.write(EXTINF_text + "\n")
        file.write(url_extracted + "\n")
        file.close()   

#This function cleans the document title
def clean_title(title):
    # Get spidered document title
    title = str(title)
    # add url decoder
    title = urllib.parse.unquote(title)
    
    # clean problematic char from title string
    title = title.replace("/","-")
    title = title.replace("/","-")
    title = title.replace("\\","-")
    title = title.replace("\"","")
    title = title.replace("\'","")

    # final string cleansing
    title = title.strip()
    title = title.lstrip()

    return title

# url file loading and cleaning process
def get_urls_from_file(list_name, url_address):

    print("Starting loading urls")
    print("with file name: " + list_name)

    counter = 0
    i = 0

    # open file with list of url
    with open("urls.txt", "r") as file: 
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

main()