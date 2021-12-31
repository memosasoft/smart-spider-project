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
    
    url_address = []
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
        current_url = link_evaluation(current_url)
        print(current_url)
        # Is it the end of the liste
        if current_url == "" and len(url_address)<=0:
            break
        
        urls_visited.append(current_url)

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
                        # AI component
                        links = fix_link(links, current_url)
                        print(links)
        
                        check_media(links)

                        links = link_evaluation(links)
                        if links not in memory:               
                            url_address.append(links)
                            memory.append(links)
                            
                            links = links.replace("movies/details/","")
                            links = links.replace("image/details/","")
                            
                            if links not in memory: 
                                url_address.append(links)
                            
                                print("EXtracted URL : " + links)
                                memory.append(links)             
                except:
                    # Shuffle de LIST
                    pass

            hrefs = html.find_all("link")
            all_hrefs = []
            for href in hrefs:
                # print(href.get("href"))
                links = href.get("href")
                try:
                     
                    if not "http" in links:
                        # AI component
                        links = fix_link(links, current_url)
                        print(links)
                        check_media(links)

                        links = link_evaluation(links)
                        
                        if links not in memory:               
                            url_address.append(links)
                            memory.append(links)
                            
                            links = links.replace("movies/details/","")
                            links = links.replace("image/details/","")
                            
                            if links not in memory: 
                                url_address.append(links)
                            
                                print("EXtracted URL : " + links)
                                memory.append(links)

                    
                    urls_visited = save_urls_from_file(urls_visited)

                except:
                    print("MAIN LOOP FAILURE") 
    
    
        except:
            print("MAIN LOOP FAILURE") 
        
            # Shuffle de LIST
            import random
            random.shuffle(url_address)
            
    # open file with list of url
    url_address = save_urls_from_file(url_address)
    url_address =  get_urls_from_file("urls.txt", url_address)

    # Recursive function
    main()
        
def fix_link(url, current_url):
    
    print("fixing link: " + url)

    if (url.find('//')==0):
        url = "https:" + url
    if (url.find('/')==0):
        url = current_url + url
    if (url.find('#')==0):
        url = ""
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
    file = url_extracted.split("/")[-1] 
    
    ext = url_extracted.split(".")[-1] 
    # Dump invalid urls
    # Request the profile picture of the OP:
    import wget
    #Now use this like below,
    save_path = './media/'
    if url_extracted not in memory:
        wget.download(url_extracted, save_path + file[0:14] +"."+ ext)
        wget.downmemoryload(url_extracted, save_path + filename)
  
    print("MEDIA FOUND SAVED")

    
    from six.moves.html_parser import HTMLParser
    h = HTMLParser()
    
    print(h.unescape(title))
    title = h.unescape(title)
    title = clean_title(title)
    
    # Dump invalid urls
    with open("ARCHIVE.M3U", "a") as file:    
        print("VOD FOUND")
        print("VOD url: " + url_extracted)
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

    i = 0
    counter = 0
    memory = []

    url_address = []

    # open file with list of url
    with open("urls.txt", "r") as file: 
        # reading each line     
        for url in file: 
            
            # Clean the url string
            url = endode_url(url)
            counter = counter + 1
                 
            # inset in url list object 
            
            if url not in memory:
                url_address.append(url)
                memory.append(url)

            if (counter>10000):
                counter = 0
                i= i + 1
                print("Urls loaded : " + str(i*10000))
    
        file.close()
   
    lines =""
    with open("urls.txt", "wb") as file: 
        file.writelines(lines)
        file.close()

    memory = []

    return url_address

# url file loading and cleaning process
def save_urls_from_file(url_address):
    memory = []
    # open file with list of url
    with open("urls.txt", "a") as file: 
        # reading each line     
        for url in url_address: 
            if url not in memory:
                file.write(str(url))
                memory.append(str(url))
        file.close()
    return url_address

# url file loading and cleaning process
def save_urls_from_file(url_address):
    memory = []
    
    # open file with list of url
    with open("urls_visited.txt", "a") as file: 
        # reading each line     
        url = ""
        file.write(str(url)+"\n")
        file.close()

    # open file with list of url
    with open("urls_visited.txt", "a") as file: 
        # reading each line     
        for url in url_address: 
            if url not in memory:
                file.write(str(url)+"\n")
                memory.append(str(url))
        file.close()
    return url_address

# This function cleans urls liste from doubles and visited links
def endode_url(url):
    # Clean the url string
    url = str(url.strip())
    return url

def link_evaluation(links):
    print(links)

    if ".org" in links:
        return links

    if ".pdf" in links:
        links = ""
    if ".txt" in links:
        links = ""
    if ".zip" in links:
        links = ""

    if ".css" in links:
        links = ""
    if ".js" in links:
        links = ""
    if ".gif" in links:
        links = ""
    if ".jpg" in links:
        links = ""
    if ".bmp" in links:
        links = ""
    if "@" in links:
        links = ""  
    if ".png" in links:
        links = ""   
    if ".ico" in links:
        links = ""  

    if "details" in links:
        return links
    if "movie" in links:
        return links
    if "upload" in links:
        return links
    if ".html" in links:
        return links
    if ".php" in links:
        return links

    if "post" in links:
        links = "" 
    if "poster" in links:
        links = "" 
    if "about" in links:
        links = "" 
    if "print" in links:
        links = "" 
    if "build" in links:
        links = "" 
    if "display" in links:
        links = "" 
    if "software" in links:
        links = "" 
    if "text" in links:
        links = "" 
    if "audio" in links:
        links = "" 
    if "service" in links:
        links = "" 
    if "view" in links:
        links = ""            
    
    if "facebook" in links:
        links = "" 
    if "google" in links:
        links = "" 
    if "microsoft" in links:
        links = "" 
    if "linke" in links:
        links = "" 
    if "youtube" in links:
        links = "" 
    if "lifewire" in links:
        links = "" 

    hit = 0

    for i in links.split("/"):
        hit = hit + 1

    # URL death value
    if (hit>=9):
        links = ""
        hit = 0

    return links 

main()

# A VPN can solve this problem 
# Proton VPN can help : https://protonvpn.com/

def simple_proxy_request(url):

    import requests
    session = requests.Session()

    session.proxies = {
        'http': 'http://10.10.10.10:8000',
        'https': 'http://10.10.10.10:8000',
    }
   
    response = requests.post(url, headers={'User-Agent': ua.random}, proxies=proxies, timeout=120)

def rotative_proxy_request(request_type, url, **kwargs):

    import requests

    ip_addresses = [ "mysuperproxy.com:5000", "mysuperproxy.com:5001", "mysuperproxy.com:5100", "mysuperproxy.com:5010", "mysuperproxy.com:5050", "mysuperproxy.com:8080", "mysuperproxy.com:8001", 
    "mysuperproxy.com:8000", "mysuperproxy.com:8050" ]

    while True:
        try:
            proxy = random.randint(0, len(ip_addresses) - 1)
            proxies = {"http": ip_addresses(proxy), "https": ip_addresses(proxy)}
            response = requests.get(request_type, url, proxies=proxies, timeout=5, **kwargs)
            print(f"Proxy currently being used: {proxy['https']}")
            break
        except:
            print("Error, looking for another proxy")
   
    return response
