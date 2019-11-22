

```python
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
from phpbb_scraper import soup_converter
from phpbb_scraper import html_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
from phpbb_scraper import url_generator
import phpbb_scraper.persistence as persistence

```


```python
help(PhpbbScraper)
```

    Help on class PhpbbScraper in module phpbb_scraper.scraper:
    
    class PhpbbScraper(builtins.object)
     |  Class for scraping phpBB Classes
     |  
     |  Class methods defined here:
     |  
     |  __init__(base=None, debug=False, wait_time=None, user=None, password=None) from builtins.type
     |      constructor
     |  
     |  get_data(session, url) from builtins.type
     |      scrapes data from url and returns it as beautiful soup object
     |  
     |  get_login_url() from builtins.type
     |      get the url for log in
     |  
     |  get_session() from builtins.type
     |      initiates session, requires credentials
     |  
     |  set_authentication(user, password) from builtins.type
     |      activate debug info display
     |  
     |  set_base_url(base_url) from builtins.type
     |      setting base url
     |  
     |  set_debug(debug=True) from builtins.type
     |      activate debug info display
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  DEBUG = False
     |  
     |  base_url = 'https://<base_url>'
     |  
     |  headers = {'User-Agent': 'Mozilla/5.0'}
     |  
     |  login_address = 'ucp.php?mode=login'
     |  
     |  password = '<password>'
     |  
     |  payload = {'login': 'Anmelden', 'password': '<password>', 'redirect': ...
     |  
     |  user = '<user>'
     |  
     |  wait_time = 5
    
    


```python
help(scraper)
```

    Help on module phpbb_scraper.scraper in phpbb_scraper:
    
    NAME
        phpbb_scraper.scraper - module to scrape contents from phpbb page also handles login into phpbb page
    
    CLASSES
        builtins.object
            PhpbbScraper
            ScraperExecutor
        
        class PhpbbScraper(builtins.object)
         |  Class for scraping phpBB Classes
         |  
         |  Class methods defined here:
         |  
         |  __init__(base=None, debug=False, wait_time=None, user=None, password=None) from builtins.type
         |      constructor
         |  
         |  get_data(session, url) from builtins.type
         |      scrapes data from url and returns it as beautiful soup object
         |  
         |  get_login_url() from builtins.type
         |      get the url for log in
         |  
         |  get_session() from builtins.type
         |      initiates session, requires credentials
         |  
         |  set_authentication(user, password) from builtins.type
         |      activate debug info display
         |  
         |  set_base_url(base_url) from builtins.type
         |      setting base url
         |  
         |  set_debug(debug=True) from builtins.type
         |      activate debug info display
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |  
         |  DEBUG = False
         |  
         |  base_url = 'https://<base_url>'
         |  
         |  headers = {'User-Agent': 'Mozilla/5.0'}
         |  
         |  login_address = 'ucp.php?mode=login'
         |  
         |  password = '<password>'
         |  
         |  payload = {'login': 'Anmelden', 'password': '<password>', 'redirect': ...
         |  
         |  user = '<user>'
         |  
         |  wait_time = 5
        
        class ScraperExecutor(builtins.object)
         |  Implementation of some frequently used scraping queries
         |  
         |  Class methods defined here:
         |  
         |  __init__(base=None, debug=False, wait_time=5, user=None, password=None, config_file=None, target_dir=None, meta_file=None) from builtins.type
         |      constructor
         |  
         |  close_session() from builtins.type
         |      close session
         |  
         |  get_session() from builtins.type
         |      gets/creates class session
         |  
         |  get_soup(url) from builtins.type
         |      retrieves soup for given url, configuration needed to be setup
         |      if url is a list, a list of soup will be returned
         |  
         |  get_soups(urls) from builtins.type
         |      reads multiple urls in case soup contains number of entries tags and a "start" property, 
         |      url will not be read. returns a list of dictionary with entry 
         |      {hash(soup_id):{'url':<url>,'url_hash':<url_hash>,'soup':<soup>,'soup_id':<soup_id>,'date':<date>}} 
         |      soup_id is concatenation of Date and url hash <JJJJMMDD_HHMMSS>_<url_hash>
         |  
         |  read_topics_from_meta(meta_file=None, target_dir=None) from builtins.type
         |      reads all soup files referenced in meta file and trasnforms soups in list of metadata attributes, alongside with data from file
         |      attributes from post gets the prefix 'post' , file metadata gets the prefix 'source'. Usually, target_dir (source of soup files)
         |      and meta_file (file containing metainformation of soup files) is set upon instanciation of this class, but can be overwritten
         |      by the parameters
         |  
         |  retrieve_last_topics(past_days=14, start_num=0, steps_num=2, increment_num=70, file_extension='html', target_dir=None, meta_file=None) from builtins.type
         |      gets the last topics from forum (across multiple pages) and saves each to an html
         |      file locally. 
         |      Parameters (default)
         |      past_days (14) - retrieve topics from last past_days
         |      start_num (0) / steps (3) start index of post, number of subsequent pages to be scraped
         |      increment_num (70) increase number of post index between pages, for default values we will
         |      be reading posts on three pages (0...69),(70...139),(140...209) 
         |      file_extension ("html")
         |      target_dir (save path) directory to save (can also be configured in config file)
         |      returns list of metadata dictionary of each soup
         |  
         |  save_topics_as_html_table(html_file=None, path=None, append_timestamp=True) from builtins.type
         |      reads topics from loval html files and transforms posts into an html table 
         |      for given path and file name. If append_timestamp is set to true, a timestamp will be added to
         |      the filename
         |  
         |  set_config_from_file(config_file) from builtins.type
         |      sets configuration from json file, having the following content:
         |      {
         |          "user": <user>,
         |          "password": <password>,
         |          "base":<url base of phpbb forum>
         |          "target_dir":<save directory>
         |          "meta_dir":<directory containing list of soup files>
         |      }
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |  
         |  DEBUG = False
         |  
         |  QUERIES = None
         |  
         |  base_url = 'https://<base_url>'
         |  
         |  meta_file = None
         |  
         |  password = '<password>'
         |  
         |  target_dir = None
         |  
         |  user = '<user>'
         |  
         |  wait_time = 5
   
    
    
    


```python
help(soup_converter)
```

    Help on module phpbb_scraper.soup_converter in phpbb_scraper:
    
    NAME
        phpbb_scraper.soup_converter - module to transform phpbb html code into beautiful soup objects
    
    FUNCTIONS
        convert_datetime(date_string, date_format='%A %d. %B %Y, %H:%M')
            converts date string of format WEEKDAY DD. MONTH YYYY, HH:MM into date format
        
        get_author_meta_from_soup(soup, debug=False, show_soup=False)
            transforms header columns of author list into dictionary
            html input
            <thead>
                <tr>
                <th class="name" data-dfn="Rang, Benutzername">
                   <span class="rank-img">
                     <a href="./memberlist.php?mode=&amp;sk=m&amp;sd=d">Rang</a>
                    </span>
                    <a href="./memberlist.php?mode=&amp;sk=a&amp;sd=a">Benutzername</a>
                </th>
                <th class="posts">
                  <a href="./memberlist.php?mode=&amp;sk=d&amp;sd=d#memberlist">Beitraege</a>
                </th>
                <th class="info">Website</th>
                <th class="joined">
                  <a href="./memberlist.php?mode=&amp;sk=c&amp;sd=a#memberlist">Registriert</a>
                </th>
            </tr>
            </thead>
            output dictionary structure (per table column): 
            [
            {'class': 'name', 'link': './memberlist.php?mode=&sk=m&sd=d', 'text': 'RangBenutzername'}, 
            {'class': 'posts', 'link': './memberlist.php?mode=&sk=d&sd=d#memberlist', 'text': 'Beiträge'}, 
            {'class': 'info', 'link': None, 'text': 'Website'}, 
            {'class': 'joined', 'link': './memberlist.php?mode=&sk=c&sd=a#memberlist', 'text': 'Registriert'}
            ]
        
        get_author_ref_from_soup(soup, debug=False, show_soup=False)
            transforms phpbb search results of author reference attributes into list of dictionary objects
            html input
            <tr class="bg1"|"bg2"> 
                <td><span class="rank-img"></span>
                    <a href="./memberlist.php?mode=viewprofile&amp;u=_user_" class="username">_username_</a>
                </td>
                <td class="posts">
                    <a href="./search.php?author_id=_user_&amp;sr=posts" title="Posts for given user">
                    _number of posts_</a>
                </td>
                <td class="info">&nbsp;|
                     <div><!-- m -->
                     <a class="postlink" href="_link_">_link_</a>
                     <!-- m --></div>
                </td>
                <td>_DATE OF REGISTRATION_</td>
            </tr>
            output dictionary structure (per table column): 
                ["rank-img",member,member_link]
                ["posts",Number of Posts,member_link]
                ["info",None,website link]
        
        get_hash(s)
            calculates a hash string of transferred string
        
        get_link_data_from_soup(soup)
            extracts url and link text from soup link snippet
            <a class="topictitle" href="https://...">_text_</a>
        
        get_num_topics(soup)
            reads number of topics, by searching for a specific text snippet
        
        get_posts_from_soup(soup, debug=False, show_soup=False)
            transforms phpbb search results (with texts) as soup objects into list of dict objects
            Search for single posts including texts
            URL https://forum_url/search.php?keywords=xxxSearchxxx&terms=all&author=&sc=1
                 &sf=titleonly&sr=posts&sk=t&sd=d&st=90&ch=300&t=0&submit=Suche
            html input (one search result is div "search post bg*"):
            <div class="search post bg1">
                <div class="inner">
                    <dl class="postprofile">
                        <dt class="author">xxxAuthorxxx
                           <a href="./memberlist.php?mode=viewprofile&amp;u=<uname>"class="username">xxxUSERNAMExxx</a>
                        </dt>
                                    <dd class="search-result-date">Date</dd>
                                    <dd>Forum: <a href="./viewforum.php?f=xxxForumNumberxxx">xxxForumTopicxxx</a></dd>
                                    <dd>Topic: <a href="./viewtopic.php?
                            f=26&amp;t=xxxForumTopicxxx;
                            hilit=xxxHiLitxxx">xxxTopixTitlexxx</a></dd>
                                    <dd>Antworten: <strong>xxxNumAnswersyyy</strong></dd>
                                    <dd>Zugriffe: <strong>xxxNumAccessxxx</strong></dd>
                            </dl>
                            <div class="postbody">
                                    <h3><a href="./viewtopic.php?f=xxxForumNumberxxx&amp;t=xxxTopicNumxxx&amp;
                        p=xxxPageNumxxxx&amp;hilit=xxxHiLitxxx#pxxxPageNumxxx">xxxTopicTitlexxx</a></h3>
                                    <div class="content">xxxContentTextExtractxxx</div>
                            </div>      
                            <ul class="searchresults">
                                    <li>
                                           <a href="./viewtopic.php?f=26&amp;t=xxxtopicxxx&amp;p=xxxPagexxx&amp; 
                            hilit=Vollformat#xxxPageNumxxx" class="arrow-right">
                                            <i class="icon fa-angle-right fa-fw icon-black" 
                                aria-hidden="true"></i><span>Call</span>
                                            </a>
                                    </li>
                            </ul>       
                    </div>
            </div>      
            
            <div class="search post bg2">   
            ...
            </div> 
            output dictionary structure: 
               ['Author',xxxUSERNAMExxx,<author_url>]
               ['Forum',xxxForumTopicxxx,<forum_url>]
               ['Topic',xxxTopicxxx,<topic_url>]
               ['Antworten',xxxNumAnswersyyy,None]
               ['Zugriffe',xxxNumAccessxxx,None]
        
        get_search_result_data_from_soup(soup, debug=False, show_soup=False)
            reads soup for header data like number of hits,search term, search url
            input html snippet:
            <h2 class="searchresults-title">Die Suche ergab ... Treffer: <a href="..search_url..">"..Title.."</a></h2>
            <p>Suchanfrage: <strong>..search_term..</strong></p>       
            output dictionary structure: 
            ..search_url..   -> search_url
            ..Title..        -> search_text
            ### Treffer      -> search_hits
        
        get_topics_from_soup(soup, debug=False, show_soup=False)
            transforms phpbb search results (topics/header only) as soup objects into list of dict objects
            Search for single posts including texts
            URL https://forum_url/search.php?keywords=xxxSearchxxx&terms=all&author=&sc=1
                &sf=titleonly&sr=topics&sk=t&sd=d&st=90&ch=300&t=0&submit=Suche
            html input (one search result is div "search post bg*"):
            <li class="row bg2">
            <dl class="row-item topic_read_hot">
            <dt title="Es gibt keine neuen ungelesenen Beitraege in diesem Thema.">
                <div class="list-inner">
                    <a href="./viewtopic.php?f=..." class="topictitle">...5</a><br />                            
                    <div class="responsive-show" style="display: none;">
                        Letzter Beitrag von <a href="./memberlist.php?mode=viewprofile..." class="username">...</a> 
                        <a href="./viewtopic.php?f=..." title="Gehe zum letzten Beitrag">...date...</a>
                        <br />Verfasst in <a href="./viewforum.php?...">...</a>
                    </div>
                    <span class="responsive-show left-box" style="display: none;">Antworten: ...</span>
                    <div class="responsive-hide left-box">
                        <i class="icon fa-paperclip fa-fw" aria-hidden="true"></i>                                
                        von <a href="./memberlist.php?mode=viewprofile&amp;...." class="username">...</a> 
                        &raquo; date information &raquo; 
                        in <a href="./viewforum.php?f=...">...</a>
                    </div>                                                    
                </div>
                </div>
            </dt>
            <dd class="posts">... <dfn>Antworten</dfn></dd>
            <dd class="views">... <dfn>Zugriffe</dfn></dd>
            <dd class="lastpost">
                <span>
                    <dfn>Letzter Beitrag </dfn>von 
                    <a href="./memberlist.php?mode=viewprofile..." class="username">...</a>
                    <a href="./viewtopic.php?f=9&amp;t=..." title="Gehe zum letzten Beitrag">
                    <i class="icon fa-external-link-square fa-fw icon-lightgray icon-md" aria-hidden="true"></i>
                    <span class="sr-only"></span>
                    </a>
                    <br />... date ...
                </span>
            </dd>
            </dl>
            </li>
            output dictionary structure: 
                ["Thema",last_post_title,last_post_link]
                ["Antworten",num_replies,None]
                ["Zugriffe",num_access,None]
                ["Datum",thread_start_datetime,None]   
                ["Author",user_name,user_id_link]
                ["Author_Aenderung",last_user_name,last_user_id_link]
                ["Datum_Aenderung",last_post_datetime,None] 
                ["Forum",forum_name,forum_id_link]
        
        is_logged_in(soup)
            checks from code snippet whether user is logged in
            phpbb signatures
            Not Logged in 
            <a href="./ucp.php?mode=login" title="Anmelden" accesskey="x" role="menuitem">
                <i class="icon fa-power-off fa-fw" aria-hidden="true"></i><span>_log on message_</span>
            </a>
            Logged in 
            <a accesskey="x" href="./ucp.php?mode=logout&amp;sid=__sid__" role="menuitem" title="log off message">
            <i aria-hidden="true" class="icon fa-power-off fa-fw"></i><span>_log off message_</span>
            </a>
        
        post_info_as_dict(post_info)
            converts list into dictionary (key,value,link)
        
        read_soup(url, base_url=None, debug=False)
            reads html content from local file or website and transforms it into soup. if base url is given, relative links will be replaced by 
            absolute links
        
        read_soup_from_local_html(filename, debug=False)
            reads html content from local file and transforms it into soup
        
        read_soup_from_url(url, wait_time=10, debug=False)
            reads html content from given url and transforms it into soup
        
        replace_relative_links(soup, base_url, debug=False)
            replaces relative link occurences starting with './' by base url
        
        soup_has_ajax_error(soup)
            checks if soup contains attributes containing data-ajax error
    
    FILE
        <lib_location>\soup_converter.py
    
    
    


```python
help(html_converter)
```

    Help on module phpbb_scraper.html_converter in phpbb_scraper:
    
    NAME
        phpbb_scraper.html_converter - utility module to transform data into html
    
    FUNCTIONS
        dict_as_html(dict_list, debug=False)
            returns dictionary as html file. keys are header lines, data 
            is assumed of format <key>:{value:<value>,link:<link>}
        
        dict_as_html_simple(dict_list, debug=False)
            returns dictionary as html file. keys are header lines, data 
            is assumed of format {<key>:<value>}
        
        dict_with_key_as_html(topics_dict_list, debug=False)
            Generates HTML table for a list of dictionaries, extracts key values from 1st line. if a key has a corresponding key 
            with suffix _link, this entry will be treated as link (and value generated as url). If a key ends with url
            the value will also be treated as link.
            source dictionary is assumed of structure
            {keyX:{subkey1:valueX1,subkey2:valueX2,....},keyY:{subkey1:valueY1,subkey2:valueY2,....}}
        
        get_html_table(table_data)
            creates  an html table, expects list of lists (rows and columns)
        
        get_link(link, text)
            gereates link
        
        wrap(content, tag, lf=False)
            embeds content string with html tags
        
        wrap_multiple(*items, tag='td', lf=False)
            wraps items in a list into html tags
    
    FILE
        <lib_location>\html_converter.py
    
    
    


```python
help(url_generator)
```

    Help on module phpbb_scraper.url_generator in phpbb_scraper:
    
    NAME
        phpbb_scraper.url_generator - Class PhpbbUrlGenerator generates URL for reading phpbb web pages
    
    CLASSES
        builtins.object
            PhpbbUrlGenerator
        
        class PhpbbUrlGenerator(builtins.object)
         |  generates URL for reading phpbb web pages
         |  
         |  Class methods defined here:
         |  
         |  __init__(base=None, debug=False) from builtins.type
         |      Initialize self.  See help(type(self)) for accurate signature.
         |  
         |  get_default_query_params() from builtins.type
         |      generate default settings for phpbb query parameters
         |  
         |  get_query_param(query_param_key) from builtins.type
         |      input one of query url params > output: dictionary value
         |  
         |  get_query_url(query=None, base=None, sort_by=None, sort_order=None, search_type=None, search_forum=None, search_result=None, num_chars=None, days=None, terms=None, author=None, start=None, member_list=False, active_topics=False) from builtins.type
         |      constructs final url for generating phpbb urls
         |  
         |  get_query_url_iterator(query=None, base=None, sort_by=None, sort_order=None, search_type=None, search_forum=None, search_result=None, num_chars=None, days=None, terms=None, author=None, start=0, num_steps=3, increment=15, member_list=False, active_topics=False) from builtins.type
         |      constructs iterator returning 'num_steps' number of urls with increasing 'start' param starting with 'start', 
         |      increasing by 'increment'
         |  
         |  set_base_url(base_url) from builtins.type
         |      setting base url
         |  
         |  set_debug(debug=True) from builtins.type
         |      activate debug info display
         |  
         |  ----------------------------------------------------------------------
         |  Data descriptors defined here:
         |  
         |  __dict__
         |      dictionary for instance variables (if defined)
         |  
         |  __weakref__
         |      list of weak references to the object (if defined)
         |  
         |  ----------------------------------------------------------------------
         |  Data and other attributes defined here:
         |  
         |  ACTIVE_TOPICS = {'search_id': 'active_topics'}
         |  
         |  ACTIVE_TOPICS_QUERY_PARAMS = {'sd': 'd', 'search_id': 'active_topics',...
         |  
         |  AUTHOR = {'author': ''}
         |  
         |  DEBUG = False
         |  
         |  DEFAULT_QUERY_PARAMS = {'author': '', 'ch': '200', 'keywords': '', 'sc...
         |  
         |  DISPLAY_NUM_CHARACTERS = {'ch': '200'}
         |  
         |  DISPLAY_POSTS = {'sr': 'posts'}
         |  
         |  DISPLAY_TOPICS = {'sr': 'topics'}
         |  
         |  KEYWORDS = {'keywords': ''}
         |  
         |  MEMBER_LIST_QUERY_PARAMS = {'sd': 'd', 'sk': 'c', 'start': '0'}
         |  
         |  QUERY_PARAMS_DICT = {'ACTIVE_TOPICS': {'search_id': 'active_topics'}, ...
         |  
         |  QUERY_PARAM_AUTHOR = 'author'
         |  
         |  QUERY_PARAM_DAYS = 'st'
         |  
         |  QUERY_PARAM_KEYWORDS = 'keywords'
         |  
         |  QUERY_PARAM_NUM_CHARS = 'ch'
         |  
         |  QUERY_PARAM_SEARCH_FORUM = 'sc'
         |  
         |  QUERY_PARAM_SEARCH_ID = 'search_id'
         |  
         |  QUERY_PARAM_SEARCH_RESULT = 'sr'
         |  
         |  QUERY_PARAM_SEARCH_TYPE = 'sf'
         |  
         |  QUERY_PARAM_SORT_BY = 'sk'
         |  
         |  QUERY_PARAM_SORT_ORDER = 'sd'
         |  
         |  QUERY_PARAM_START = 'start'
         |  
         |  QUERY_PARAM_TERMS = 'terms'
         |  
         |  SEARCH_ALL = {'sf': 'all'}
         |  
         |  SEARCH_FIRST_POST = {'sf': 'firstpost'}
         |  
         |  SEARCH_FORUM_ONLY = {'sc': '0'}
         |  
         |  SEARCH_PAST_7DAYS = {'st': '7'}
         |  
         |  SEARCH_PAST_DAYS = {'st': '0'}
         |  
         |  SEARCH_SUBFORUM = {'sc': '1'}
         |  
         |  SEARCH_TITLE = {'sf': 'titleonly'}
         |  
         |  SEARCH_TOPIC = {'sf': 'msgonly'}
         |  
         |  SORT_ASCENDING = {'sd': 'a'}
         |  
         |  SORT_BY_AUTHOR = {'sk': 'a'}
         |  
         |  SORT_BY_CREATION_DATE = {'sk': 't'}
         |  
         |  SORT_BY_FORUM = {'sk': 'f'}
         |  
         |  SORT_BY_POST = {'sk': 's'}
         |  
         |  SORT_BY_RANK = {'sk': 'm'}
         |  
         |  SORT_BY_REGISTRATION = {'sk': 'c'}
         |  
         |  SORT_BY_TOPIC = {'sk': 'i'}
         |  
         |  SORT_DESCENDING = {'sd': 'd'}
         |  
         |  START_POSITION = {'start': '0'}
         |  
         |  TERMS_ALL = {'terms': 'all'}
         |  
         |  TERMS_ANY = {'terms': 'any'}
         |  
         |  base_url = 'https://<base_url>'
         |  
         |  memberlist_address = 'memberlist.php'
         |  
         |  search_address = 'search.php'
    
    FILE
        <lib_location>\url_generator.py
    
    
    


```python
help(PhpbbUrlGenerator)
```

    Help on class PhpbbUrlGenerator in module phpbb_scraper.url_generator:
    
    class PhpbbUrlGenerator(builtins.object)
     |  generates URL for reading phpbb web pages
     |  
     |  Class methods defined here:
     |  
     |  __init__(base=None, debug=False) from builtins.type
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  get_default_query_params() from builtins.type
     |      generate default settings for phpbb query parameters
     |  
     |  get_query_param(query_param_key) from builtins.type
     |      input one of query url params > output: dictionary value
     |  
     |  get_query_url(query=None, base=None, sort_by=None, sort_order=None, search_type=None, search_forum=None, search_result=None, num_chars=None, days=None, terms=None, author=None, start=None, member_list=False, active_topics=False) from builtins.type
     |      constructs final url for generating phpbb urls
     |  
     |  get_query_url_iterator(query=None, base=None, sort_by=None, sort_order=None, search_type=None, search_forum=None, search_result=None, num_chars=None, days=None, terms=None, author=None, start=0, num_steps=3, increment=15, member_list=False, active_topics=False) from builtins.type
     |      constructs iterator returning 'num_steps' number of urls with increasing 'start' param starting with 'start', 
     |      increasing by 'increment'
     |  
     |  set_base_url(base_url) from builtins.type
     |      setting base url
     |  
     |  set_debug(debug=True) from builtins.type
     |      activate debug info display
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  ACTIVE_TOPICS = {'search_id': 'active_topics'}
     |  
     |  ACTIVE_TOPICS_QUERY_PARAMS = {'sd': 'd', 'search_id': 'active_topics',...
     |  
     |  AUTHOR = {'author': ''}
     |  
     |  DEBUG = False
     |  
     |  DEFAULT_QUERY_PARAMS = {'author': '', 'ch': '200', 'keywords': '', 'sc...
     |  
     |  DISPLAY_NUM_CHARACTERS = {'ch': '200'}
     |  
     |  DISPLAY_POSTS = {'sr': 'posts'}
     |  
     |  DISPLAY_TOPICS = {'sr': 'topics'}
     |  
     |  KEYWORDS = {'keywords': ''}
     |  
     |  MEMBER_LIST_QUERY_PARAMS = {'sd': 'd', 'sk': 'c', 'start': '0'}
     |  
     |  QUERY_PARAMS_DICT = {'ACTIVE_TOPICS': {'search_id': 'active_topics'}, ...
     |  
     |  QUERY_PARAM_AUTHOR = 'author'
     |  
     |  QUERY_PARAM_DAYS = 'st'
     |  
     |  QUERY_PARAM_KEYWORDS = 'keywords'
     |  
     |  QUERY_PARAM_NUM_CHARS = 'ch'
     |  
     |  QUERY_PARAM_SEARCH_FORUM = 'sc'
     |  
     |  QUERY_PARAM_SEARCH_ID = 'search_id'
     |  
     |  QUERY_PARAM_SEARCH_RESULT = 'sr'
     |  
     |  QUERY_PARAM_SEARCH_TYPE = 'sf'
     |  
     |  QUERY_PARAM_SORT_BY = 'sk'
     |  
     |  QUERY_PARAM_SORT_ORDER = 'sd'
     |  
     |  QUERY_PARAM_START = 'start'
     |  
     |  QUERY_PARAM_TERMS = 'terms'
     |  
     |  SEARCH_ALL = {'sf': 'all'}
     |  
     |  SEARCH_FIRST_POST = {'sf': 'firstpost'}
     |  
     |  SEARCH_FORUM_ONLY = {'sc': '0'}
     |  
     |  SEARCH_PAST_7DAYS = {'st': '7'}
     |  
     |  SEARCH_PAST_DAYS = {'st': '0'}
     |  
     |  SEARCH_SUBFORUM = {'sc': '1'}
     |  
     |  SEARCH_TITLE = {'sf': 'titleonly'}
     |  
     |  SEARCH_TOPIC = {'sf': 'msgonly'}
     |  
     |  SORT_ASCENDING = {'sd': 'a'}
     |  
     |  SORT_BY_AUTHOR = {'sk': 'a'}
     |  
     |  SORT_BY_CREATION_DATE = {'sk': 't'}
     |  
     |  SORT_BY_FORUM = {'sk': 'f'}
     |  
     |  SORT_BY_POST = {'sk': 's'}
     |  
     |  SORT_BY_RANK = {'sk': 'm'}
     |  
     |  SORT_BY_REGISTRATION = {'sk': 'c'}
     |  
     |  SORT_BY_TOPIC = {'sk': 'i'}
     |  
     |  SORT_DESCENDING = {'sd': 'd'}
     |  
     |  START_POSITION = {'start': '0'}
     |  
     |  TERMS_ALL = {'terms': 'all'}
     |  
     |  TERMS_ANY = {'terms': 'any'}
     |  
     |  base_url = 'https://<base_url>'
     |  
     |  memberlist_address = 'memberlist.php'
     |  
     |  search_address = 'search.php'
    
    


```python
help(persistence)
```

    Help on module phpbb_scraper.persistence in phpbb_scraper:
    
    NAME
        phpbb_scraper.persistence - "Persistence module to store/access scraped data. So far, only a minimal json based persistence is implemented
    
    FUNCTIONS
        append_json(filename, dict_entries, debug=False)
            appends dictionary data to a json file as UTF-8 on file system 
            by reading file contents, deleting the old file and writing old content 
            with new content on a new file with the same file name
            opens file with 'w' (open as new or create)
        
        copy_file(source, target, force_delete=False)
            copies source to target file, in case target file exits, force_delete either
            will prevent copy or force a delete of previous file and copy of source file
        
        create_filename(filename, path=None, file_extension=None, append_timestamp=False)
            helper method to create a filename based on name, path , file extension and option
            to append a timestamp
        
        read_html_file_names(path, debug=False)
            reads recursively html files from file directly
        
        read_json(filename, debug=False)
            reads a given json file (UTF-8 format) from file system. Returns data as string
        
        read_json_as_dict(filename, debug=False)
            reads a given json file (UTF-8 format) from file system. Returns data as dictionary
            transform each json entry:
            {"<key>": "<value>",   "link": "<link>"} into dictionary entry
            {<key>:{"value":<value>,"link":<link>}}
        
        save_data(data, filename, path=None, file_extension=None, append_timestamp=False, encoding='utf-8')
            saves data as string to file, optional with appended timestamp, returns path
    
    FILE
        <lib_location>\persistence.py
    
November 2019, aiventures    
    
