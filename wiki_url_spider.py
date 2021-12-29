# Python program to AI smart spider project
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import urllib.parse

RELAX_TIME = 1.5

#This function gets html and text data from wikipedia
def getUrl():

    url_spider_count = 0
    url_error_count = 0
    
    url_address = []
    urls_found = []
    urls_session_found = []

    print("WELCOME TO wiki-smart-url-spider")       
    print("Starting text mining")
    print("Simple Python 3 program ")    
    print("Developped Doctor g. ") 
    print("help: gfm@gmail.com\n")
  
    print("LOADING MEMORY")
    print("PLEASE WAIT...")
    
    # open file with list of url
    url_address =  get_urls_from_file("urls.txt", url_address)
    
    relax(RELAX_TIME)
    
    print("STARTING WIKI TEXT SPIDER PROCESS")
        
    # loop thru array of urls
    for current_url in url_address:
        
        print("NEW LOOP")
        # if url was allready downloaded
        if current_url in urls_session_found:
            continue

        print("GETTING URL : " + current_url)
        
        try:
            # get html file
            res = requests.get(current_url)
            html_page = res.content

        except:
            print("requests Error in REQUEST IN getUrl()")   
            continue

        print("STARTING TEXT EXTRACTION PROCESS")
        # HTML content processing
        soup_spider = BeautifulSoup(html_page, 'html.parser')
        page_html_content = soup_spider.find_all(text=True)

        output = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            'css',
            'link',
            'javascript',
            # there may be more elements you don't want, such as "style", etc.
        ]

        for item in page_html_content:
            if item.parent.name not in blacklist:
                try:
                    this_string = str(item)
                    output += str(this_string)
                except:
                    print("BeautifulSoup parsing error converting html to text")
                    
                    
        # SAVE TITLE AND ORIGINAL TXT
        # DOCUMENT FOR FUTUR PROCESSING  
        print("saving url txt format")
        spider_doc_title = clean_title(current_url)
        save_url_content(spider_doc_title, output, ".txt", "./spider/")

        # SAVE HTML TITLE AND ORIGINAL   
        print("saving url html format")
        save_url_content(spider_doc_title, html_page, ".html", "./spider_html/")

        # counters for stats and program result interpretation
        url_spider_count = url_spider_count + 1

        # output to help understand program flow
        print("Spider document title: " + str(spider_doc_title))  
        
        # Spider cadence
        relax(RELAX_TIME)

        # output to help understand program flow
        print("STARTING URL EXTRACTION FROM HTML FILE DOWNLOADED")

        # extracting process
        urls_found = extractUrls(current_url, url_spider_count, url_error_count, urls_found)

        # output to help understand program flow
        print("Starting url cleaning process...")
        print("")

        # save visited url to visited memory list object
        if not current_url in urls_session_found:
            urls_session_found.append(current_url)
            print("Adding url to session list...")
        
        # dump url memory in file from urls_found array
        for url_item in urls_found:
            if url_item in urls_session_found:
                url_item = endode_url(url_item)
                print("Double global list url found!")
                print("url: " + str(url_item))
                urls_found.remove(url_item)

        # dump url memory in file from urls_found array
        urls_found_double_verification = []
        
        for url_item in urls_found:
            urls_found_double_verification.append(url_item)
            urls_found = remove_url_double(urls_found, url_item)

        urls_found = urls_found_double_verification

        count_urls = 0
        for url_item in urls_found:
            count_urls = count_urls + 1

        print("Cleaning process completed...")
        print("Unique urls found: " + str(count_urls))
        print("Winting 10 sec before next loop...")

        # Spider cadence
        relax(RELAX_TIME)

#This extracts de urls from the wiki page
def extractUrls(current_url, url_spider_count, url_error_count, urls_found):
    
    html = current_url # your HTML
    html_page = ""
    urls_invalid_found = []
    
    current_url = str(current_url)
    
    try:
        res = requests.get(current_url)
        html_page = res.content
    except:
        print("requests Error in extractUrls()")   
        return url_error_count, urls_found    
    
    soup_spider = BeautifulSoup(html_page, 'html.parser')
    
    # open file with list of url   
    with open("urls.txt", "a") as file:
        # stats
        url_good_count = 0
        url_total_count = 0
        url_total_invalid_count = 0
        spider_error_total_count = 0
        null_link_total_count = 0
        url_total_root_count = 0

        # url containers
        url_extracted = ""
        url_original = ""

        # link extraction
        for item in soup_spider.find_all('a'): 
            try:
                # Extract the url from the html tag
                url_extracted = str(item.get('href'))
                
                # First url check
                if url_extracted == "None":
                    null_link_total_count = null_link_total_count + 1
                    continue 
                
                # keep a copy of the url for later processing
                url_original = url_extracted
            except:
                print("Extraction Error - Url extraction with extraction module") 
                spider_error_total_count = spider_error_total_count + 1
                url_total_count += 1
            
            # url check
            if url_extracted.find("/wiki/Wikipedia") == 0:
                url_total_invalid_count += 1
                url_total_count += 1
                urls_invalid_found = set_invalid_url(url_original, urls_invalid_found)

                # go to the next url in html doc
                continue
    
            # url check
            if url_extracted.find(":")>0:
                url_total_invalid_count += 1
                url_total_count += 1
                urls_invalid_found = set_invalid_url(url_original, urls_invalid_found)

                # go to the next url in html doc
                continue
            
            # url check
            if url_extracted.find("/wiki/Main_Page") == 0:
                url_total_invalid_count += 1
                url_total_count += 1
                urls_invalid_found = set_invalid_url(url_original, urls_invalid_found)

                # go to the next url in html doc
                continue
            
            # url check
            if url_extracted.find("#") == 0:
                url_total_invalid_count += 1
                url_total_count += 1
                urls_invalid_found = set_invalid_url(url_original, urls_invalid_found)

                # go to the next url in html doc
                continue

            # url check
            if url_extracted.find("//") == 0:
                url_total_invalid_count += 1
                url_total_count += 1
                urls_invalid_found = set_invalid_url(url_original, urls_invalid_found)

                # go to the next url in html doc
                continue
            
            # url check
            if url_extracted.find("/wiki/") == 0:
                print("url: " + url_extracted)
                
                url_found = False
                if not url_extracted in urls_found:
                    file.write('https://en.wikipedia.org' + url_extracted + "\n")
                    urls_found.append(url_extracted)
                    url_good_count += 1
                    url_total_count += 1
                    continue
            else: 
                url_total_invalid_count += 1
                url_total_count += 1
                urls_invalid_found = set_invalid_url(url_original, urls_invalid_found)

        file.close()

    # Dump invalid urls
    with open("urls_invalid.txt", "a") as file:    
        for url_invalid in urls_invalid_found:
            file.write(url_invalid + "\n")
        file.close()

    print("Invalid urls added...")
    relax(RELAX_TIME)

    # Dump visited urls
    with open("urls_visited.txt", "a") as file:    
        file.write(current_url + "\n")
        file.close()

    print("Visited urls added...")
    print("url: " + str(current_url))

    relax(RELAX_TIME)

    # Spider crawling process stats and info
    print("Number of pages spidered: " + str(url_spider_count))
    print("Error spidered page count: " + str(url_error_count))
    print("Error spider: " + str(spider_error_total_count))
    print("None links: " + str(null_link_total_count))
    print("url good hits: " + str(url_good_count))
    print("total invalid urls: " + str(url_total_invalid_count))
    print("total urls: " + str(url_total_count))
    print("Winting 10 sec before next spider crawl.")
    
    # Spider cadence
    relax(RELAX_TIME)

    return urls_found

# ivalid url check and processing
def set_invalid_url(url_original, urls_invalid_found):
    if url_original[0:4] != "http":
        url_original = 'https://en.wikipedia.org' + str(url_original.strip().lower())

    if not url_original in urls_invalid_found:
        urls_invalid_found.append(url_original)

    return urls_invalid_found

#This function read the texte
def save_url_content(spider_doc_title, output, ext, save_path ):
    try:     
        # open file with list of url
        with open(str(save_path) + str(spider_doc_title) + str(ext), "w") as file:
            file.write(output)
            file.close()
    except:
        print("Error in save_url_content()")   

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
    with open(list_name, "r") as file: 
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

def relax(s):
    time.sleep(s)

# url file loading and cleaning process
# clean_urls_list("urls.txt")

# start the url extraction
# start the html extraction
getUrl()