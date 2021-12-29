#!/usr/bin/env python
from bs4 import BeautifulSoup

## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import datetime # needed to create unique image file name
import time # needed to create unique image file name
import mimetypes # needed for download functionality

urls_buffer = [] # program main url buffer
images_tags = [] # program main found url/link buffer

image_urls = []

# Content container for image extraction process memory
downloaded_images_for_content = []
downloaded_images_url_for_content = []

urls_links  = [] # buffer
urls_visited  = [] # visited_links

# keywords container for query and page content
query_keywords = []
content_keywords = []

# stop words and urls for blocking urls
stop_words = []
stop_urls = []

response_container = ""

# Software parameter for twiking system images retrieval
RELAX_TIME = 10
MIN_LINK_LENGTH = 10
MIN_KEYWORD_LENGTH = 5
MIN_KEYWORDS_IN_LINK = 3
MIN_CONTENT_LENGTH = 7

# CONTENT QUALITY PARAMETERS
DIFFICULTY_RATIO = 20
URL_CONTENT_QUALITY_SCORE = 50
CONTENT_QUALITY_SCORE = 100

# LEARNING FUNCTIONALITY NOT YET IMPLEMENTED
SMART_ERROR_SWITCH = 0
STABILIZER = 0

def init_program():
   
    print("WELCOME to smart spider 2.0")       
    print("Python search agent research program")    
    print("Memosasoft.ml - Memosa Services")
    print("gfm.mail.72@gmail.com")
    
    # user interaction to clean urls lists 
    start_user_interaction()
    
    query = input("What type of content do you want to spider?")
       
    # get url start with search engine API retruns list of urls
    search_engine(query)
    
    # build query and content verification keyword list
    build_keywords_lists(query)
    
    relax(RELAX_TIME)
    
def build_keywords_lists(query):
    
    # Quality score used to decide if the url matches keywords of query
    global CONTENT_QUALITY_SCORE
    global DIFFICULTY_RATIO
    global content_keywords
    global query_keywords
    
    print("GETTING START URLS FROM API... ")
    relax(RELAX_TIME) 
    
    for keywords in query.split():
        keywords = keywords.lower()
        keywords = trim(keywords)
        keywords = str(keywords)
        keywords = clean_word_final(keywords)
        #keywords = clean_stop_list(keywords)
        
        if not keywords in query_keywords:
            
            if (len(keywords)>=MIN_KEYWORD_LENGTH):
                
                if not keywords in query_keywords:
                    query_keywords.append(keywords)
                    
                if not keywords in content_keywords:    
                    content_keywords.append(keywords)
                
                print("Adding keywords: ")
                print(keywords)
                                      
                # ADDING WORD WITHOUT S AT THE END
                if (keywords[len(keywords)-1]=="s"):
                    if not keywords[len(keywords)-1] in query_keywords:
                        query_keywords.append(keywords[0:len(keywords)-1])  
                    if not keywords[len(keywords)-1] in content_keywords:          
                        content_keywords.append(keywords[0:len(keywords)-1])
                    
                    print(keywords[0:len(keywords)-1])
                
                # ADDING WORD ROOT FOR BETTER MATCHING          
                if (len(keywords)>=6):
                    if not keywords[0:3] in query_keywords:
                        query_keywords.append(keywords[0:3])
                    if not keywords[0:3] in content_keywords:   
                        content_keywords.append(keywords[0:3])
                    print(keywords[0:3])
                
                # add root of the word 
                if (len(keywords)>=12):
                    if not keywords[0:6] in query_keywords:
                        query_keywords.append(keywords[0:6])
                    if not keywords[0:6] in content_keywords:
                        content_keywords.append(keywords[0:6])
                    print(keywords[0:6])
                   
    new_list = []
    for phrase in content_keywords:
        for word in phrase.split():
            new_list.append(word) 
    
    content_keywords.clear()

    for word in new_list:
        content_keywords.append(word)                              
    
    # add extra query keywords to find images
    sticky_keyword()
    
    print("Calculation query quality limit score")
    CONTENT_QUALITY_SCORE = CONTENT_QUALITY_SCORE * (len(query_keywords)/DIFFICULTY_RATIO)
    print("CONTENT_QUALITY_SCORE is " + str(CONTENT_QUALITY_SCORE) + "\n")

# starting list will be save to urls.txt
# each spidered url will verify html content and extract new urls to the file
# the urls.txt are the full for the spider 

def sticky_keyword():
    
    global query_keywords
    global content_keywords
    
    # adding images keywords for searching site with image content 
    query_keywords.append("3D")
    query_keywords.append("graphic")
    query_keywords.append("photo")
    query_keywords.append("photograph")
    query_keywords.append("photography")
    query_keywords.append("image")
    query_keywords.append("pictures")
    query_keywords.append("gallery")
    query_keywords.append("wallpaper")
    query_keywords.append("representation")
                  
    # adding images keywords for searching site with image content
    content_keywords.append("3D")
    content_keywords.append("graphic")
    content_keywords.append("photo")
    content_keywords.append("photograph")
    content_keywords.append("photography")
    content_keywords.append("image")
    content_keywords.append("picture")
    content_keywords.append("gallery")
    content_keywords.append("wallpaper")  
    query_keywords.append("representation")    
    
    # adding images keywords for searching site with image content 
    query_keywords.append("article")
    query_keywords.append("text")
    query_keywords.append("video")
    query_keywords.append("reference")
    query_keywords.append("graph")
                  
    # adding images keywords for searching site with image content
    content_keywords.append("article")
    content_keywords.append("text")
    content_keywords.append("video")
    content_keywords.append("reference")
    content_keywords.append("graph") 
    
def search_engine(query):
    # PSEUDO CODE 
    # Connect to search apiload_urls_from_memory_from_search_api
    # Bring back urls from search api
    print("Connecting to search API")
    
    # loop thru search api 5
    max_loop = [1]
    print("Building keywords list object")
        
    for loop in max_loop:
        print("Connecting to API")
        response = connect_search_api(query, loop)

        #relax(RELAX_TIME)   
        # save found url to urls.txt file
        f = open("urls.txt", "a")
            
        for search_results in response["value"]:
            search_url = search_results["url"]
            #print("\n\n_____________________________________________________")
            #print("\nkeywords to memory content verification list")
            #print("\nAdding keywords: " + search_results["title"])
            content_keywords.append(search_results["title"])           
            #print("\nurl to the url buffer list")
            #print("\nurl: " + search_url)
            f.write(search_url + "\n")          
            #relax(RELAX_TIME)
        f.close()

def start_user_interaction():
    
    user_input = input("Clean urls files? (y/n)")
    
    if (user_input=="y"):
        clean_url_file()
        
    # clean images folders
    user_input = input("Clean images folders? (y/n)")
       
    if (user_input=="y") or (user_input=="Y"): 
        
        user_input = input("Partial clean up or full cleanup? (p)artial/(f)ull")
        
        if (user_input=="p") or (user_input=="P"): 
            delete_images("partial")
    
        if (user_input=="f") or (user_input=="F"):        
            delete_images("full")
            
    user_input = input("Delete html files?")
    
    if (user_input=="y") or (user_input=="Y"): 
        delete_html_in_folders()
    
def clean_url_file():
    with open("urls.txt", "w", encoding="utf-8") as file:
        file.write("")
    with open("urls_visited.txt", "w", encoding="utf-8") as file:
        file.write("")
    with open("urls_images.txt", "w", encoding="utf-8") as file:
        file.write("")
        
def delete_images(switch):
    import os, re, os.path
    
    mypath = "./images/"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))

def delete_html_in_folders():
    import os, re, os.path
    
    mypath = "./data/"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
            
    mypath = "./spider/"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))
     
def start_spider():
   
    global urls_buffer 
    global urls_visited
       
    print("Loading memory...\n")
      
    # Load image-miner url memory 
    load_urls_from_memory("urls_visited.txt", urls_visited)
    load_urls_from_memory("urls.txt", urls_buffer)
    
    #relax(RELAX_TIME)   
    print("Memory loaded")
    print("Starting mining process...")
    
    for url in urls_buffer:
        
        print("START NEW SPIDER PROCESS...")
        print("PROCESSING URL: " + url)
        
        # check url stop list 
        # to block spider to process unwanted sites 
        print("FIRST CHECK")
        print("Checking if url contains stop list keywords")    
        
        if (check_url_for_stop_keyword(str(url))):
            
            print("URL is clean no unwanted keywords in url - PASSED") 
                    
            if not url in urls_visited: 
                print("Url not in visited list verification - PASSED")
                relax(RELAX_TIME)
            else:
                print("Url is in visited list - FAILED")
                urls_buffer.remove(url)
                continue     
        else:
            print("URL is dirty contains stopwords - FAILED") 
            urls_buffer.remove(url)
            continue
    
        print("Url verified for stopwords url and previously visited sites - ALL TESTS PASSED")
        print("Url can be downloaded")
        print("DOWNLOADING URL: " + url)
        relax(RELAX_TIME)
                
        # Get url
        try:
            html_file = get(url)
        except:
            print("ERROR DOWNLOADING URL")
            continue
        
        if (verify(html_file)):
            continue
        
        print("Adding url to visited memory...")
        if not url in urls_visited:
            urls_visited.append(url)
    
        print("EXTRACTING URL TEXTUAL CONTENT")
        # get content
        page_text = get_content(html_file)
                    
        # Is the site worth downloading
        content_verification_flag = False
         
        print("VERIFYING CONTENT...") 
        # verify the content and should the page be saved to memory
        if not verify_page_content(url, page_text):
            
            print("Site passed content verification...")
            save_html_data(url, html_file)
            
            # Site has good content
            content_verification_flag = True
        else:
            print("Site failed content verification skipping...")
            print("URL EXTRACTION PROCESS - WILL BE IGNORED")
            print("IMAGE EXTRACTION PROCESS - WILL BE IGNORED")
            continue
                        
        try:
                   
            print("STARTING URL EXTRACTION PROCESS ")
            relax(RELAX_TIME) 
            
            urls_extraction_process(url, html_file)             
            images_extraction_process(url, html_file)
        
        except:
            print("ERROR in url or image extraction")
                
        # Save content page with title, content and images
        try:
            # if the content has good content 
            # extract info from site
            if content_verification_flag:
                print("Saving html content")
                worked = save_html_info(url, html_file)
            else:
                print("Saving html content will not be saved")
        except:
            print("ERROR in save_html_info(url, html_file)")
            print("url: " + url)
            print("INFORMATION EXTRACTION - FAILED")
        
        # global cleanup to eliminate 
        print("\n\nCALLING FINAL CLEANUP PROCESS\nwith: " + url + "\n\n")  
        cleanup()
        
    # Recursive function will never stop
    start_spider()

def urls_extraction_process(url, html_file):
    
    # extract url
    urls_links = extract_urls(url, html_file)

    # insert in session eliminating duplicate links
    for found_url in urls_links:

        if found_url in urls_buffer:
            while found_url in urls_links:
                urls_links.remove(found_url)
                continue
            
        if found_url in urls_visited:
            while found_url in urls_links:
                urls_links.remove(found_url)
                continue
                    
        if not found_url in urls_buffer:
            if not found_url in urls_visited:
                print("Url link found: " + found_url)
                urls_buffer.append(found_url)   
            
def images_extraction_process(url, html_file):
    print("\nSTARTING IMAGE EXTRACTION PROCESS ")
    print(url + "\n")   
    
    relax(RELAX_TIME)
    
    # extract image
    images_tags = extract_images(url, html_file)
    
    print("\n\nIMAGE LINK EXTRACTION SUCCESS\nwith: " + url + "\n")
            
    # insert in session eliminating duplicate links
    for img in images_tags:
        if not img in image_urls:
            image_urls.append(img)
            get_image(img)
        else:
            print("Image is ignored all ready spidered test - FAILED \n\n")
                                    
# IDEALLY THE SYSTEM SHOULD CONNECT TO GOOGLE AND BING SEARCH ENGINES
def connect_search_api(query, page_number):
    
    URL = "https://rapidapi.p.rapidapi.com/api/Search/WebSearchAPI"
    HEADERS = {
        'x-rapidapi-key': "e2c4e6deabmsh054a7dd9082d6f9p1dddc2jsn9fa43d149a24",
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }

    query = query
    page_number = page_number
    page_size = 10
    auto_correct = True
    safe_search = False
    
    # val = input("Is this the query: " + query)

    querystring = {"q": query,
                "pageNumber": page_number,
                "pageSize": page_size,
                "autoCorrect": auto_correct,
                "safeSearch": safe_search}
    
    response = requests.get(URL, headers=HEADERS, params=querystring).json()

    total_count = response["totalCount"]

    for web_page in response["value"]:

        url = web_page["url"]
        title = web_page["title"]
        description = web_page["description"]
        body = web_page["body"]
        date_published = web_page["datePublished"]
        language = web_page["language"]
        is_safe = web_page["isSafe"]
        provider = web_page["provider"]["name"]

        #print("title: {}".format(title))
        #print("Url: {}...".format(url))
   
    return response

def cleanup():       
    # Save all visited urls
    
    print("Saving urls.txt")
    print("Saving urls_visited.txt")
    relax(RELAX_TIME)
    
    print("cleaning urls memory")
    relax(RELAX_TIME)
    
    # create a clean list
    clean_list = []
    
    # Rebuild the session list and clean
    for url in urls_buffer:
        if not url in urls_visited:
            clean_list.append(url)               

    # Empty session url list
    urls_buffer.clear()
        
    # Rebuild the session list and clean
    for url in clean_list:
        if not url in urls_visited:
            urls_buffer.append(url)   
    
    save_urls(urls_buffer, "urls.txt")
    save_urls(urls_visited, "urls_visited.txt")
    
    print("\nCLEANING PROCESS COMPLETED - PASSED\n\n")
    relax(RELAX_TIME)
            
def load_urls_from_memory(filename, urls_list):
    
    # read url file 
    with open(filename) as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            if not line in urls_list:
                urls_list.append(trim(line))
    
    # debug - function information        
    return urls_list
   
def get(url):
    # Getting the webpage, creating a Response object.
    response = requests.get(url)
    
    # Extracting the source code of the page.
    html_file = response.text
    return html_file

def save_html_data(url, html_file):
    print("\nWriting url to disk")

    filedate = datetime.datetime.now()
    filename = filedate.strftime("spider-%Y%M%H%S%f.html")
    # filename = filename + original_filename
    
    with open("./spider/" + filename , "w", encoding="utf-8") as file:
        file.write(html_file)
   
    relax(RELAX_TIME)

def relax(sec):
    time.sleep(sec) 

def get_image(url):
    
    global image_urls
    
    import os

    try:        
        ## Set up the image URL and filename
        filename = url.split("/")[-1]
        # file name creating with timestamp
        filename = datetime.datetime.now()
        filename = filename.strftime("img-%Y%M%H%S%f") 
        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(url, stream = True)
        ext = get_extension(r)
        filename = filename + "." + ext
        
        if ext == "shtml":
            print("IMAGE IS NOT AN IMAGE - shtml")
            return False
        
        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
                        
            # Because image was downloaded add it to visited links
            if not url in urls_visited:
                urls_visited.append(url)
                
            if not url in image_urls: 
                image_urls.append(url)
            
            # Eliminate url from main urls buffer - Rethink NOT really needed 
            while url in urls_buffer:   
                urls_buffer.remove(url)
                
            # Open a local file with wb ( write binary ) permission.
            with open("./buffer/" + filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)        
                
            try:   
                fileSize = os.path.getsize("./buffer/" + filename)
                #relax(RELAX_TIME)   
                
                if (ext == "mp4"):
                    shutil.move("./media/mp4" + filename, './media/mp4')
                if (ext == "mp3"):
                    shutil.move("./media/mp3" + filename, './media/mp3')
                    
                if (fileSize>=100000):
                    shutil.move("./buffer/" + filename, './buffer/../images/')
                    print('Downloaded: ' + filename)
                    downloaded_images_for_content.append("./buffer/" + filename)
                    downloaded_images_url_for_content.append(url)
                    
                elif (fileSize>=50000) and (fileSize<100000):
                    shutil.move("./buffer/" + filename, './buffer/../images/')
                    print('Downloaded: ' + filename) 
                    downloaded_images_for_content.append("./buffer/" + filename)
                    downloaded_images_url_for_content.append(url)
                      
                #elif (fileSize>500) and (fileSize<50000):
                    #shutil.move("./images/" + filename, './images/small_images') 
                #else:
                    #shutil.move("./images/" + filename, './images/very_small_images') 
                
                relax(RELAX_TIME/6)  
                
                mypath = "./buffer/"  
                for root, dirs, files in os.walk(mypath):
                    for file in files:
                        os.remove(os.path.join(root, file))
                        mypath = "./buffer/"   
            except:
                print("FILE CLASSIFICATION depending of size ERROR")
                relax(RELAX_TIME)  
                    
            return True
        else:
            print('Image Couldn\'t be retreived')
            relax(RELAX_TIME)  
                
            return False
    except:
        print('MAJOR EXCEPTION - Image Couldn\'t be retreived')
        return None   
         
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
        'script',
        'meta',
        'div'
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def save_html_info(url, html_page):
    
    # html content list
    html_document = []
    
    try:
        html_document = extract_html_content(url, html_page)
    except:
        print("ERROR in extract_html_content(url, html_page)")
    
    try:
        url, title, description, keywords, headings, paragraphs =  html_document 
    except:
        print("ERROR unpacking html_document")
        
    if (len(title)>MIN_CONTENT_LENGTH) and (len(description)>MIN_CONTENT_LENGTH):
        if (len(url)>MIN_CONTENT_LENGTH) and (len(keywords)>MIN_CONTENT_LENGTH):
            print("Information missing to save content memory file")
            return False
    
    try:
    
        dateTimeObj = datetime.datetime.now()
    
        # open file with list of url
        f = open(dateTimeObj.strftime("./spider/" +"web-%Y%S%f.html"), "w")
        f.write("<html>")
        f.write("<title>" + str(title) + "</title>")
        f.write("<head>")
        f.write("</head>")
        f.write("<body>")
        f.write("<b>Title:</b><h1> " + str(title) + "</h1><br><br>")
        f.write("<b>Description:</b> " + str(description) + "<br><br>")
        
        if (len(keywords)>5):
            f.write("<b>Keywords:</b>  " + str(keywords) + "<br><br>")
        
        f.write("<b>url:</b>  <a href=\"" + str(url) + "\">" + str(url) + "</a><br><br>")
        f.write(str(headings) + "<br><br>")
        
        try:
            if (len(paragraphs) > 0):
                f.write(str(paragraphs[0]) + "<br><br>")
        except:
            print("ERROR in spider html paragraph section")
        
        index = 0
        
        for img in downloaded_images_for_content:
            f.write("<br><div width=\"50%\" height=\"auto\"><img src=\"" + downloaded_images_url_for_content[index]+ " width=\"100px\" height=\"auto\" \"><br></div><br>")
            f.write("<br><div width=\"50%\" height=\"auto\"><a href=\"" + downloaded_images_url_for_content[index]+ " width=\"100px\" height=\"auto\" \">Link</a><br></div><br>")
            
            index = index + 1
            
        f.write("</body></html>")
        f.close()
        
        # TODO - CONVERT FORMAT TO JSON
        save_registry(url, title, description)
        
    except:
        print("ERROR in saving output to file") 
        
    return True

def extract_html_content(url, html_page):
    
    html_document = []
    
    try:  
          
        title =""
        description = ""
        keywords = ""
        headings = ""
        paragraphs = []
        d_quality = 0
        
        soup_spider = BeautifulSoup(html_page, 'html.parser')

        for title in soup_spider.find_all('title'):
            title = title.get_text() 
            print("Title: " + title)
            d_quality = d_quality + 10
            
        for link in soup_spider.findAll(attrs={"name":"description"}):
            
            link = link.get("content")
            
            if link == None:
                break
            
            #print(link)
            description = description + " " + str(link)
            print("Description: " + description)
            d_quality = d_quality + 5
            
        for link in soup_spider.findAll(attrs={"name":"keywords"}):

            link = link.get("content")
            
            if link == None:
                break
            
            #print(link)
            keywords = keywords + " <b>" + str(link) + "</b>"
            print("Keywords: " + keywords)
            d_quality = d_quality + 5
            
        # Read all headings            
        # creating a list of all common heading tags
        heading_tags = ["h1", "h2", "h3", "h4", "h5", "h5"]
        
        for tags in soup_spider.find_all(heading_tags):
            headings = headings.capitalize() + "<b>" + tags.text.strip() + "</b><br>";
            d_quality = d_quality + 2
            
        # Read all paragraph
        for paragraph in soup_spider.find_all("p"):
            paragraphs.append(paragraph.text.strip())
            d_quality = d_quality + 1
        
    except:
        print("Error in first section of save_html_info") 
        
    if (d_quality>URL_CONTENT_QUALITY_SCORE):  
        html_document = [url, title, description, keywords, headings, paragraphs]  
        print("QUALITY SCORE: " + str(d_quality) + " - PASSED")   
    else:
        html_document = [url, title, description, keywords, headings, paragraphs]  
        print("QUALITY SCORE: " + str(d_quality) + " - FAILED")   
   
    return html_document

def save_registry(url, title, description): 
    # read url file
    f = open("registry.txt", "a")
    f.write("url: " + url + " - " + "title: " + title + " - " + "description: " + description + "\n")
    f.close()
    
def summarize(text):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
        return text  
    
    sentences = sent_tokenize(text)
    sentenceValue = dict()    
    
    for sentence in sentences:
        for wordValue in freqTable:
            if wordValue[0] in sentence.lower():
                if sentence[:12] in sentenceValue:
                    sentenceValue[sentence[:12]] += wordValue[1]
                else:
                    sentenceValue[sentence[:12]] = wordValue[1]
                
    sumValues = 0
    
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
        
    # Average value of a sentence from original text
    average = int(sumValues/ len(sentenceValue))

    summary = ''
    for sentence in sentences:
        if sentence[:12] in sentenceValue and sentenceValue[sentence[:12]] > (1.5 * average):
            summary +=  " " + sentence
            
    return summary

def debug_info(info): 
    # read url file
    f = open("debug.txt", "a")
    f.write(info)
    f.close()

def load_stop_list():
    global stop_words 

    with open("stop_list.txt","r") as file: 
    # reading each line"
        for word in file:
            word = word.replace("\n","")
            word = trim(word)
            stop_words.append(word)

def word_size(text, size):    
    rebuild_text = ""    
    # preformating word     
    for word in text.split():    
        if len(word)<size:
            rebuild_text =  rebuild_text  
        else:
            rebuild_text =  rebuild_text + " " + word 
        
    return rebuild_text
           
def clean_stop_list(word):    
        
    # preformating word     
    if word in stop_words:    
        return ""   
    return word

def clean_word_final(word):
    index = 0
    for char in word:
        # ^ is the references char
        if char in "()[]{},.-:;|*/+\"\\~^":
            word = word.replace(char, " ")
        index = index + 1
    
    word = trim(word)
    return word

def verify_link(link):
    global query_keywords
    global i_score

    print("LINK VERIFICATION")
    
    i_score = 0
        
    for keyword in query_keywords:
        
        link = link.lower()
        
        if (link.find(keyword.lower())>=0):
            
            print("MATCH keyword is " + keyword)
            
            if (len(keyword)>MIN_KEYWORD_LENGTH):
                
                i_score = i_score + 1
                
                if (i_score > MIN_KEYWORDS_IN_LINK-1):
                    
                    print("ACCEPTED LINK - QUERY KEYWORD MATCH SCORE : " + str(i_score))   
                    print("URL: " + link)     
                    print("MATCHING KEYWORDS FOUND IN LINK - PASSED") 
                    
                    return True
                
    for keyword in content_keywords:

        link = link.lower()
        
        if (link.find(keyword.lower())>=0):
            
            print("MATCH keyword is " + keyword)
            
            if (len(keyword)>MIN_KEYWORD_LENGTH):
                
                i_score = i_score + 1
                
                if (i_score > MIN_KEYWORDS_IN_LINK-1):
                    
                    print("ACCEPTED LINK - EXTRA CONTENT KEYWORD MATCH SCORE : " + str(i_score))   
                    print("URL: " + link)     
                    print("MATCHING KEYWORDS FOUND IN LINK - PASSED") 
                    
                    return True
    print("NO MATCHING KEYWORDS FOUND IN LINK - FAILED") 
    return False  
    
def verify_page_content(url, text):
     
    print("STARTING PAGE CONTENT VERIFICATION")
    print("Checking url: ")
    print("url: " + url)
       
    global content_keywords
    global i_score
    
    i_score = 0
    
    keywords = []
    keyword_match_matrix = []
    
    for items in content_keywords:
        for word in items.split():
            word = word.lower()
            word = trim(word)
            word = str(word)
            
            word = clean_word_final(word)
            word = clean_stop_list(word)
            
            if (len(word)>MIN_KEYWORD_LENGTH): 
                if not word in keywords:
                    #print(word)
                    keywords.append(word)
                    
                    # add keyword without s at the end
                    if (keywords[len(keywords)-1]=="s"):
                        keywords.append(word[0:len(keywords)-1])
                        
                    # add root word
                    keywords.append(word[0:6])
             
    for keyword in text.split():
        
        # normalize keyword 
        keyword = keyword.lower()
        keyword = trim(keyword)
        keyword = str(keyword)
        
        # keyword clean and stop list
        keyword = clean_word_final(keyword)
        keyword = clean_stop_list(keyword)
        
        if (len(keyword)>MIN_KEYWORD_LENGTH): 
            
            if keyword in query_keywords:
                i_score = i_score + 5
                
                if not keyword in keyword_match_matrix:
                    keyword_match_matrix.append(keyword)
                                
            if keyword in keywords:
                i_score = i_score + 1
                
                if not keyword in keyword_match_matrix:
                    keyword_match_matrix.append(keyword)
                
    if i_score > CONTENT_QUALITY_SCORE:
        print("URL PASSES QUALITY SCORE: " + str(i_score))  
        return False
                    
    print("FINAL QUALITY SCORE: " + str(i_score))        
    print("QUALITY SCORE TEST - FAILED")        
    
    return True

def get_content(html):
    try:
        content = ""
        paragraphs = []
  
        soup_spider = BeautifulSoup(html, 'html.parser')

        for title in soup_spider.find_all('title'):
            content = title.get_text() 

        for link in soup_spider.findAll(attrs={"name":"description"}):
            
            link = link.get("content")
            
            if link == None:
                break
            
            #print(link)
            content = content + " " + str(link)
            
        for link in soup_spider.findAll(attrs={"name":"keywords"}):

            link = link.get("content")
            
            if link == None:
                break
            
            #print(link)
            content = content + " " + str(link)
        
        # Read all headings            
        # creating a list of all common heading tags
        heading_tags = ["h1", "h2", "h3"]
        
        for tags in soup_spider.find_all(heading_tags):
            print(tags.name + " -> " + tags.text.strip())
            content = content + tags.name + " -> " + tags.text.strip() + "\n";
    
        # Read all paragraph
        for paragraph in soup_spider.find_all("p"):
            
            paragraphs.append(paragraph.text.strip())
            
            content = content + " " + paragraph.text.strip()
        
    except:
        print("Error in first section of save_html_info")  
        return content 

    return content 

# this function extract urls or img from a url
# it returns a list of urls or images tags
def extract_urls(url, html): 
    
    try:
        
        urls_links = []
        
        print("\nSTARTING URL EXTRACTION PROCESS\n")
        relax(RELAX_TIME) 
        
        print("\nStarting SOUP\n")
        soup = BeautifulSoup(html, "html.parser")
        
        for link in soup.find_all("a"):
            
            try:    
                link = link.get("href")
                
                print(link)
                
                if link in urls_visited:
                    print("Link has all ready been downloaded in visited list memory")
                    continue
                
                # Check if the url is long enoughs to process
                print("____________________________________________")       
                print("\n\nVERIFY size of url")        
                print("URL: " + link)
                
                if (len(link)<MIN_LINK_LENGTH):
                    print("\ninvalid link length to small - FAILED")
                    #relax(RELAX_TIME) 
                    continue
                
                print("SIZE OF THE LINK - PASSED")
                #relax(RELAX_TIME) 
                
                # Rebuild the site if the url root is missing
                if not link is None:
                    root_path = ""
                    if link.find("http")<0:
                        # get root https path
                        root_path = get_path(url, link)
                        
                        if not root_path in urls_buffer:
                            print("Adding root path\n" +  root_path)
                            urls_buffer.append(root_path)
                            
                        if link[0] == "/":
                            link = root_path + link
                        else:
                            link = root_path + "/" + link  
                            
                print("\nROOT PATH VERIFICATION - PASSED")
                print("URL: " + link)
                #relax(RELAX_TIME) 
                        
                if verify_link(link):
                    print("\nLink verification test - PASSED\n\n")
                    print("URL: " + link)
                    #relax(RELAX_TIME)
                    urls_links.append(link)
                else:
                    continue
    
            except:
                print('ERROR EXCEPTION - extract() sub section link = link.get(sub_tag)')
                print(link)
                relax(RELAX_TIME)
                 
            if not link in urls_links:
                if (link != url):
                    
                    try:
                        if (check_url_for_stop_keyword(link)):
                            print("\n\nStop list test - PASSED\n\n")
                            #relax(RELAX_TIME)
                        else:
                            print("\n\nStop list test - FAILED\n\n")
                            continue
                        
                        print("new link found:\n" + link)
                        
                        if not link in urls_buffer:
                            print("ADDING TO MAIN URL BUFFER\n\n" + link)
                            urls_buffer.append(link)
                            #relax(RELAX_TIME) 
 
                    except:
                        print('MAJOR EXCEPTION URLS - extract_urls() sub section link in links')
                        relax(RELAX_TIME)  
        
        return urls_links
    except:
        print('MAJOR EXCEPTION URLS - extract_urls()')
        relax(RELAX_TIME)  
        
        return urls_links
    
# this function extract urls or img from a url
# it returns a list of urls or images tags
def extract_images(url, html): 
    
    # Images stats
    numLink = 0 
    
    try:    
        img_links = []
        
        print("\n\nPROCESSING image tags extraction: \nURL: " + url + "\n")        
        print("Creating soup object...")
                     
        soup = BeautifulSoup(html, "html.parser")
   
        print("STARTING IMAGE EXTRACTION")
        
        for link in soup.find_all("img"):
            
            images = soup.findAll('img')

            
            numLink = numLink + 1
            
            link = link.get("src")
            
            try:
                for param in link:
                    img_description = param["alt"]
                    print("IMAGE DESCRIPTION: " + img_description)
            except:
                print("NO ALT INFORMATION IN IMAGE")
                 
            print("\nImage link\n\nURL: " + link)
            print("\nNumber of images " + str(numLink))
                     
            # Rebuild the site if the url root is missing
            if not link is None:
                root_path = ""
                if link.find("http")<0:
                    # get root https path
                    root_path = get_path(url, link)
                    
                    if not root_path in urls_buffer:
                        print("Adding root path\n" +  root_path)
                        urls_buffer.append(root_path)
                        
                    if link[0] == "/":
                        link = root_path + link
                    else:
                        link = root_path + "/" + link  
            
                    print("\nAFTER ROOT VERIFICATION:\nURL: " + link + "\n\n")
                    
            if verify_link(link):
                print("\nLink verification test - PASSED\n\n")
                print("URL: " + link)
            else:
                continue
                        
            if not link in img_links:
                if (link != url): 
                    try:      
                        print("\nCHEKING IMAGE LINK FOR STOP WORDS IN URL\n")
                        
                        if (check_url_for_stop_keyword(str(link))):    
                            print("\nAdding link img_links")
                            print("\nImage link passes keyword in link - PASSED ")
                            print("\nURL:" + link)  
                        else:
                            print("\nMATCH STOP WORD FOUND IN URL TEST _ FAILED")
                            print("\nThis link wont be spidered")
                            continue
             
                        if not link in image_urls:
                            img_links.append(link) 
                            print("\nImages link not in memory - PASSED")    
                        else:
                            print("\nImages will not be added allready in memory - FAILED") 
                            continue     
                    except:
                        print('\nEXCEPTION - extract_images() sub section link in links:')   
                        #relax(RELAX_TIME)    
        
        print("\nIMAGES " + numLink + " HAVE ALL BEEN EXTRACTED")
        relax(RELAX_TIME)     
        return img_links
    except:
        print('EXCEPTION - extract images')
        relax(RELAX_TIME)  
        return img_links

def clean_raw_text(url_text):
    while (url_text.find("\t")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
    
    while (url_text.find("\n")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
    
    while (url_text.find("  ")>=0):
        url_text = url_text.replace("\t", " ") 
        url_text = url_text.replace("\n", " ") 
        url_text = url_text.replace("  ", " ") 
           
    return url_text
        
def save_urls(urls, file_name): 
    # write url in visited site file
    url_memory = []
    
    with open(file_name, "w", encoding="utf-8") as file:
        for url in urls:
            if not url is None:
                if not url in url_memory:
                    file.write(url + "\n")
                if not url in url_memory:
                    url_memory.append(url) 
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

def verify(url):
    if (url == "") or (url == " ") or (url == None) or (len(url)<MIN_LINK_LENGTH):
        return True
    else:
        return False
    
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

def check_url_for_stop_keyword(url_to_check):
    
    for stop_url in stop_urls:
        
        try:
            if (url_to_check.find(stop_url)>=0):
                print("Ignoring url found match in URL check list keyword")
                print("\nUrl: " + url_to_check)
                print("Stop keyword is: " + stop_url + "\n")
                print("STOP WORD IN URL TEST - FAILED\n")
                #relax(RELAX_TIME)
                return False
        except:
            print("ERROR in check_url_for_stop_keyword()") 
            print("BECAUSE OF ERROR - STOP WORD IN URL TEST - FAILED\n")
            return False

    print("Url passed the URL check list test - PASSED")
    #relax(RELAX_TIME)
                        
    return True

def load_stop_urls():
    global stop_urls
    
    with open("stop_urls.txt","r") as file: 
                                  
        # reading each line"
        for line in file:
            line = line.replace("\n","")
            line = trim(line)
            stop_urls.append(line)
            
def trim(text_section): 
    text_section = text_section.strip()
    text_section = text_section.lstrip()
    return text_section 

def main():   
    # Start image spider/miner program
    load_stop_urls()
    load_stop_list()

    init_program()
    start_spider()
    
# start image miner 2.0    
main()