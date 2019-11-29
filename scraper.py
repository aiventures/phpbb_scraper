""" module to scrape contents from phpbb page also handles login into phpbb page"""
import requests
import re
import json
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from phpbb_scraper import persistence
from phpbb_scraper import html_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
from phpbb_scraper import soup_converter
import time
from datetime import datetime
from dateutil import parser
import traceback

class PhpbbScraper:
    """Class for scraping phpBB Classes""" 
    base_url = r"https://<base_url>"
    login_address = 'ucp.php?mode=login'
    user = "<user>"
    password = "<password>"
    wait_time = 5
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'username': user, 'password': password, 
               'redirect':'index.php','sid':'','login':'Anmelden'}
    DEBUG = False

    @classmethod                 
    def __init__(cls, base=None,debug=False,wait_time=None,
                 user=None,password=None):
        """constructor"""

        cls.DEBUG = debug
        if base is not None:
            cls.base_url = base
        if wait_time is not None:
            cls.wait_time = wait_time
        if user is not None:
            cls.user = user
        if password is not None:
            cls.password = password
        if cls.DEBUG is True:
            print("Constructor, Base set to",base)

    @classmethod    
    def set_debug(cls,debug=True):    
        """activate debug info display"""
        
        cls.DEBUG = debug    

    @classmethod    
    def set_authentication(cls,user,password):    
        """activate debug info display"""

        cls.user = user
        cls.password = password        

    @classmethod    
    def set_base_url(cls,base_url):    
        """setting base url"""
        
        cls.base_url = base_url
        if cls.DEBUG is True:
            print("base url:",base_url)          

    @classmethod    
    def get_login_url(cls):    
        """get the url for log in"""
        login_url = urlparse.urljoin(cls.base_url,cls.login_address)
        return login_url
    
    @classmethod    
    def get_session(cls):  
        """initiates session, requires credentials"""
        session_payload = cls.payload.copy()
        session_payload['username'] = cls.user
        session_payload['password'] = cls.password
        url_login = cls.get_login_url()
        try:
            with requests.Session() as session:
                login_get = session.get(url=url_login, headers=cls.headers)
                soup_login = BeautifulSoup(login_get.content, 'html.parser')
                # get sid token from login screen 
                sid = soup_login.find('input', attrs={'name': 'sid'})['value']    
                # login with parameters
                session_payload['sid'] = sid        
                #login_post = session.post(url_login, data=session_payload, headers=headers)                                        
                if cls.DEBUG is True:
                    print(f"Session login via url {url_login}, session id {sid}")
                    print("header data:",session.headers)              
                    print(f"Waiting {cls.wait_time} seconds")                            
            time.sleep(cls.wait_time)         
            return session
        except:
            print(traceback.format_exc())
            return None         

    @classmethod         
    def get_data(cls,session,url):
        """scrapes data from url and returns it as beautiful soup object"""
        try:
            scrape_data = session.get(url,headers=cls.headers)            

            if cls.DEBUG is True:
                print(f"getting data from {url}, status code {scrape_data.status_code}")                                
                #print(f"header data {scrape_data.headers}")                  
            soup = BeautifulSoup(scrape_data.text,"html.parser")                    
            time.sleep(cls.wait_time) 
            return soup
        except:
            print(traceback.format_exc())
            return None          

class ScraperExecutor:
    """Implementation of some frequently used scraping queries """

    """Class for scraping phpBB Classes""" 
    base_url = r"https://<base_url>"
    user = "<user>"
    password = "<password>"
    wait_time = 5
    DEBUG = False
    target_dir = None
    meta_file = None

    #query url params, use as litteral
    # SEARCH_PAST_DAYS, SEARCH_PAST_7DAYS
    # SORT_BY_FORUM, SORT_BY_AUTHOR, SORT_BY_CREATION_DATE, 
    # SORT_BY_TOPIC, SORT_BY_POST, SORT_BY_RANK, SORT_BY_REGISTRATION, 
    # SORT_ASCENDING, SORT_DESCENDING 
    # SEARCH_ALL, SEARCH_TOPIC, SEARCH_TITLE, SEARCH_FIRST_POST, 
    # SEARCH_FORUM_ONLY, SEARCH_SUBFORUM 
    # DISPLAY_TOPICS, DISPLAY_POSTS 
    # DISPLAY_NUM_CHARACTERS 
    # KEYWORDS 
    # TERMS_ANY, TERMS_ALL
    # AUTHOR, START_POSITION, ACTIVE_TOPICS
    QUERIES = None

    @classmethod                 
    def __init__(cls, base=None,debug=False,wait_time=5,
                 user=None,password=None,config_file=None,
                 target_dir=None,meta_file=None):
        """constructor"""    
        cls.base_url = base
        cls.user = user
        cls.password = password
        cls.wait_time = wait_time
        cls.session = None
        cls.DEBUG = debug
        cls.QUERIES = PhpbbUrlGenerator.QUERY_PARAMS_DICT.copy()
        cls.target_dir = target_dir
        cls.meta_file = meta_file
        if config_file is not None:
            cls.set_config_from_file(config_file)
    
    @classmethod                 
    def set_config_from_file(cls, config_file):                 
        """ sets configuration from json file, having the following content:
            {
                "user": <user>,
                "password": <password>,
                "base":<url base of phpbb forum>
                "target_dir":<save directory>
                "meta_dir":<directory containing list of soup files>
            }
        """

        try:
            config = persistence.read_json(filename=config_file)
            if cls.DEBUG is True:
                print(f"set config from file {config_file} contains keys {config.keys()}")
            cls.user = config.get('user')
            cls.password = config.get('password')
            cls.base_url = config.get('base')
            cls.target_dir = config.get('target_dir')
            cls.meta_file = config.get('meta_file')            
            return
        except:            
            print(traceback.format_exc())
            return        

    
    @classmethod 
    def get_soup(cls,url):
        """retrieves soup for given url, configuration needed to be setup
           if url is a list, a list of soup will be returned """
        scraper = PhpbbScraper(base=cls.base_url,debug=cls.DEBUG,wait_time=cls.wait_time,
                               user=cls.user,password=cls.password)
        session = cls.get_session()

        try:
            soup = scraper.get_data(session=session,url=url)
        except:
            print(traceback.format_exc())
            soup = None
        cls.close_session()
        return soup
    
    @classmethod 
    def get_soups(cls,urls,num_max_topics=None):    
        """ reads multiple urls in case soup contains number of entries tags and a "start" property, 
            url will not be read. returns a list of dictionary with entry 
            {hash(soup_id):{'url':<url>,'url_hash':<url_hash>,'soup':<soup>,'soup_id':<soup_id>,'date':<date>}} 
            soup_id is concatenation of Date and url hash <JJJJMMDD_HHMMSS>_<url_hash>
            max_topics will override number of maximum topics to be read
        """

        soups = {}
        first_run = True
        num_total_topics = 0

        # get datetime and datetime string
        dt = datetime.now()
        dt_string = dt.strftime("%Y%m%d_%H%M%S")        

        scraper = PhpbbScraper(base=cls.base_url,debug=cls.DEBUG,wait_time=cls.wait_time,
                               user=cls.user,password=cls.password)
        session = cls.get_session()       

        for url in urls:
            soup = None

            try:
                # get the start index 'start=xxx' of the query
                start_index = re.findall(r'start=(\d+)',url)
                if len(start_index) == 1:
                    num_start_index = int(start_index[0])                    
                else:
                    num_start_index = 0
                
                # block execution of urls with start index larger than max number of topics
                if first_run is False:
                    if ( num_total_topics > 0 ) and ( num_start_index <= num_total_topics ):
                        soup = scraper.get_data(session=session,url=url)
                    else:
                        if cls.DEBUG is True:
                            print(f"soup not read for url {url} with start index {num_start_index} of total {num_total_topics} ")
                        continue                    
            except:
                print(traceback.format_exc())

            if first_run is True:
                soup = scraper.get_data(session=session,url=url)
                first_run = False
                if num_max_topics is None:
                    num_total_topics = soup_converter.get_num_topics(soup)
                else:
                    num_total_topics = num_max_topics

                if cls.DEBUG is True:
                    print(f"Total number of Topics according to 1st run: {num_total_topics}, date/time: {dt_string}")        
            
            if soup is not None:
                if cls.DEBUG is True:
                    print(f"Adding soup for url {url} start index {num_start_index} of total {num_total_topics} ")                    
                url_hash = soup_converter.get_hash(url)
                data = {}
                data['url'] = url
                data['url_hash'] = url_hash
                data['soup'] = soup
                soup_id = dt_string + "_" + url_hash
                data['soup_id'] = soup_id                
                data['date'] = dt
                soups[soup_converter.get_hash(soup_id)] = data

        cls.close_session()
        return soups

    @classmethod 
    def retrieve_last_topics(cls,past_days=14,start_num=0,steps_num=2,increment_num=70,file_extension='html',target_dir=None,meta_file=None,num_max_topics=None):
        """ gets the last topics from forum (across multiple pages) and saves each to an html
            file locally. 
            Parameters (default)
            past_days (14) - retrieve topics from last past_days
            start_num (0) / steps (3) start index of post, number of subsequent pages to be scraped
            increment_num (70) increase number of post index between pages, for default values we will
            be reading posts on three pages (0...69),(70...139),(140...209) 
            file_extension ("html")
            target_dir (save path) directory to save (can also be configured in config file)
            returns list of metadata dictionary of each soup 
        """        
        url_gen = PhpbbUrlGenerator(base=cls.base_url,debug=cls.DEBUG)
        # Constant Definitions from url generator
        DISPLAY_TOPICS = url_gen.get_query_param('DISPLAY_TOPICS') 
        save_path = target_dir        

        if save_path is None:
            save_path = cls.target_dir
        
        if meta_file is None:
            meta_file = cls.meta_file            

        query_it = url_gen.get_query_url_iterator( search_result=DISPLAY_TOPICS,days=past_days,                                          
                                                   start=start_num,num_steps=steps_num,
                                                   increment=increment_num,active_topics=True)
        query_urls = list(query_it)                
        soups = cls.get_soups(query_urls,num_max_topics)

        metadata_list = []

        for key in soups:                            
            data = soups[key]
            data['key']=key
            filename = data['soup_id']                        
            data['filename'] = filename + '.' + file_extension
            soup = str(data.pop('soup',None) )

            if cls.DEBUG is True:
                print(f"\nProcessed soup with key {key}, filename {filename}.{file_extension} \n url {data['url']} url hash: {data['url_hash']} soup with {len(soup)} bytes and date {data['date']}")

            if save_path is not None:
                persistence.save_data(soup,filename=filename,path=save_path,file_extension=file_extension)
                if cls.DEBUG is True:            
                    print(f"saving file with name {filename}.{file_extension} to path {save_path}")
            
            metadata_list.append(data)
        
        if meta_file is not None:
            persistence.append_json(meta_file, metadata_list, debug=cls.DEBUG)

        return metadata_list

    @classmethod 
    def save_topics_as_html_table(cls,html_file=None,path=None,append_timestamp=True):
        """ reads topics from loval html files and transforms posts into an html table 
            for given path and file name. If append_timestamp is set to true, a timestamp will be added to
            the filename """
        topics = cls.read_topics_from_meta()
        html = html_converter.dict_with_key_as_html(topics)
        s = persistence.save_data(html,filename=html_file,path=path,file_extension='html',append_timestamp=True)
        print(s)

    @classmethod 
    def read_topics_from_meta(cls,meta_file=None,target_dir=None): 
        """reads all soup files referenced in meta file and trasnforms soups in list of metadata attributes, alongside with data from file
           attributes from post gets the prefix 'post' , file metadata gets the prefix 'source'. Usually, target_dir (source of soup files)
           and meta_file (file containing metainformation of soup files) is set upon instanciation of this class, but can be overwritten
           by the parameters
        """
        
        if meta_file is None:
            meta_file = cls.meta_file
        
        if target_dir is None:
            target_dir = cls.target_dir

        if ( target_dir is None ) or ( meta_file is None ):
            print("ScraperExecutor.read_topics_from_met: No metafile or target dir reference is given")
            return
                
        json_list_raw = persistence.read_json(meta_file)
        
        if len(json_list_raw) >= 1:    
            attributes = list(json_list_raw[0].keys())

        meta_data_list = {}
        processed_meta_files = []
        for json_raw in json_list_raw:
            key = json_raw.pop('key',None)
            # avoid duplicate processing
            if ( key not in processed_meta_files ) and ( key is not None ): 
                meta_data_list[key] = json_raw.copy()            
                processed_meta_files.append(key)         
        
        if cls.DEBUG is True:
            print(f"ScraperExecutor.read_topics_from_meta, number of file entries {len(processed_meta_files)}")   
        
        processed_posts = [] # avoid duplicate processing of the same posts
        post_attribute_list = {}
        double_posts = 0
        attributes_valid = ['date', 'filename', 'soup_id', 'url', 'url_hash']
                    
        if cls.DEBUG is True:
            show_info = True
        else:
            show_info = False

        # read through all soups referenced in meta list
        for meta_data_key in meta_data_list:
            source_meta = {}
            source_meta['source_key'] = meta_data_key
            meta_data = meta_data_list[meta_data_key]       
            attributes = meta_data.keys()

            # attributes from metadata per soup
            for attribute in attributes:                
                if attribute not in attributes_valid:
                    continue                
                attribute_key = 'source_' + attribute
                value = meta_data.get(attribute)
                if attribute == 'date':
                    value = parser.parse(value)
                elif attribute == 'filename':
                    value = target_dir + '\\' + value
                source_meta[attribute_key] = value
                        
            soup = soup_converter.read_soup(source_meta['source_filename'],base_url=cls.base_url,debug=cls.DEBUG)

            if soup is None:        
                print(f"Reading file {source_meta['source_filename']} failed, will be skipped")
                continue

            # analyze data 
            topic_data_list = soup_converter.get_topics_from_soup(soup, debug=cls.DEBUG)

            for topic_data in topic_data_list:             

                json_data = json.loads(topic_data)

                if show_info is True:       
                    print("****** TOPIC ENTRY (ONLY 1st is shown) ****\n")                        
                    print(f"JSON DATA: {json_data}\n")                

                post_data = {}
                post_hash = None

                for entry in json_data:                
                    link = entry.pop('link')
                    key, value = (list(entry.items())[0])        
                    key = "post_" + key.lower()
                    if 'datum' in key:
                        value = parser.parse(value)
                    post_data[key] = value
                    if link is not None:
                        key_link = key + '_link'            
                        post_data[key_link] = link
                        if key == 'post_thema':
                            post_hash = soup_converter.get_hash(link)
                        post_data.update(source_meta)
            
                if ( post_hash is not None ):
                    if post_hash not in processed_posts:            
                        processed_posts.append(post_hash)
                        post_attribute_list[post_hash] = post_data                 
                    else:
                        double_posts += 1
                
                if show_info is True:
                    print(f"transformed data with key hash {post_hash}: {post_data}")

                show_info = False

            if cls.DEBUG is True:
                print("*********************************************")
                print(f"Number of read Topics for file with hash {meta_data_key}: {len(post_attribute_list)}, Number of Duplicate Posts: {double_posts}")

        return post_attribute_list


    @classmethod 
    def get_session(cls):    
        """ gets/creates class session """

        cls.session = None
        if cls.session is None:
            scraper = PhpbbScraper(base=cls.base_url,debug=cls.DEBUG,wait_time=cls.wait_time,
                                   user=cls.user,password=cls.password)
            cls.session = scraper.get_session()
        return cls.session
    
    @classmethod 
    def close_session(cls):    
        """ close session """

        if cls.session is not None:
            cls.session.close()
            cls.session = None
        return None

    #def get_page_meta_information(cls,url):
    #    """ retrieves meta information from a phpbb site"""
    #  scraper def get_search_result_data_from_soup(soup, debug=False, show_soup=False):

    

    


