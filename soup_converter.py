""" module to transform phpbb html code into beautiful soup objects """

from datetime import datetime
from bs4 import BeautifulSoup
import hashlib
import re
import requests
import time
import locale
import traceback
import json
# use German locale; name might vary with platform
locale.setlocale(locale.LC_ALL, 'de_DE')

def get_hash(s):
    """calculates a hash string of transferred string"""
    hash_object = hashlib.md5(s.encode())
    return hash_object.hexdigest()

# convert entry to dict / expects 3 entries: key, value, link
def post_info_as_dict(post_info):
    """ converts list into dictionary (key,value,link) """

    key, value, link = post_info
    return {key: value, "link": link}

def convert_datetime(date_string, date_format='%A %d. %B %Y, %H:%M'):
    """converts date string of format WEEKDAY DD. MONTH YYYY, HH:MM into date format"""

    try:
        # Convert Dates of sort Sonntag 9. Juni 2019, 09:00 as date format
        date_obj = datetime.strptime(date_string.strip(), date_format)
    except:
        date_obj = datetime(1900, 1, 1)
        print(traceback.format_exc())
    return date_obj

# extracts link and text from <a class="topictitle" href="https://...">_text_</a>

def get_link_data_from_soup(soup):
    """extracts url and link text from soup link snippet
       <a class="topictitle" href="https://...">_text_</a>
    """

    link_data = []
    if soup == None:
        return [None, None]
    link = soup.get('href')
    text = soup.text
    if link is not None:
        link = link.strip()
    if text is not None:
        text = text.strip()        
    link_data.append(link)
    link_data.append(text)
    return link_data


def read_soup_from_url(url, wait_time=10, debug=False):
    """reads html content from given url and transforms it into soup"""

    soup = None
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        print('Reading %s , Status %d , waiting %d seconds ...' %
              (url, r.status_code, wait_time))
        time.sleep(wait_time)
    except:
        print(traceback.format_exc())
    return soup


def read_soup_from_local_html(filename, debug=False):
    """reads html content from local file and transforms it into soup"""

    print('Reading file %s' % (filename))
    try:
        with open(filename, encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, "html.parser")
        f.close()
    except:
        soup = None
        print(traceback.format_exc())
    return soup


def read_soup(url, base_url=None,debug=False):
    """reads html content from local file or website and transforms it into soup. if base url is given, relative links will be replaced by 
       absolute links """

    soup = None
    # read local file
    if debug == True:
        print("\n***********************************")
        print("Opening ", url)
    # read url or file
    if url[:4].lower() == "http":
        soup = read_soup_from_url(url, debug=debug)
    else:
        soup = read_soup_from_local_html(url, debug=debug)
    if debug is True:
        print(f"read soup from {url} containing {len(str(soup))} characters")                
    if base_url is not None:
        soup = replace_relative_links(soup,base_url,debug=debug)
    return soup

def get_num_topics(soup):
    """reads number of topics, by searching for a specific text snippet"""
    try:
        #num = int(re.search("Suche ergab (\\d+)", str(soup)).group(1))        
        num = int(re.search("(\\d+) Treffer", str(soup)).group(1))  
    except:        
        num = 0
        print(traceback.format_exc())  

    return num

# Reads number of search results, search term and link to search from snippet
# Code Snippet
# <h2 class="searchresults-title">Die Suche ergab ... Treffer: <a href="..search_url..">"..Title.."</a></h2>
# <p>Suchanfrage: <strong>..search_term..</strong></p>
def get_search_result_data_from_soup(soup, debug=False, show_soup=False):
    """reads soup for header data like number of hits,search term, search url
       input html snippet:
       <h2 class="searchresults-title">Die Suche ergab ... Treffer: <a href="..search_url..">"..Title.."</a></h2>
       <p>Suchanfrage: <strong>..search_term..</strong></p>       
       output dictionary structure: 
       ..search_url..   -> search_url
       ..Title..        -> search_text
       ### Treffer      -> search_hits

    """

    # extract code snippet with search title
    search_results_num_soup = soup.find("h2", {"class": "searchresults-title"}) 
    if show_soup is True:
        print("***   SOUP FOR SEARCH RESULT HEADER *****************")
        print(search_results_num_soup)
        print("*******************************************")
    search_results = {}

    if search_results_num_soup is not None:
        search_result_text = search_results_num_soup.text        
        try:
            search_url = search_results_num_soup.find("a").attrs['href']
        except:
            print(traceback.format_exc())
            search_result_text = None
            search_url = None
    else:
        search_result_text = None
        search_url = None
    search_results['search_url'] = search_url

    # get the search term (everything behind "Treffer: ")
    try:
        search_text = re.search('Treffer: (.*)', search_result_text).group(1)
        search_text = search_text.strip('\"')
    except:
        print(traceback.format_exc())
        search_text = None
    search_results['search_text'] = search_text

    # get the number of hits
    try:
        search_hits_reg = re.search(r'\d+', search_result_text)
        search_hits = int(search_hits_reg.group(0))
    except:
        print(traceback.format_exc())
        search_hits = 0

    search_results['search_hits'] = search_hits
    if debug is True:
        print(f"Search url {search_results['search_url']}" +
              f"\nText:{search_results['search_text']}, number hits:{search_results['search_hits']}")
    return search_results


def get_posts_from_soup(soup, debug=False, show_soup=False):
    """ transforms phpbb search results (with texts) as soup objects into list of dict objects
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
    """

    # post content of each found post
    post_data_json = []

    # extract all blocks enclosed by search post bg (followed by a number, therefore using regex)
    search_posts_soup = soup.findAll(
        "div", {"class": re.compile("^(search post bg)")})

    if debug == True:
        print("Num Search Posts:", len(search_posts_soup))

    for search_post_soup in search_posts_soup:
        if show_soup == True:
            print("$$$$$$ NEW SEARCH POST SOUP $$$$$$$$")
            print(search_post_soup)

        single_post_data = []
        if debug == True:
            print("\n########NEW SEARCH POST###########")

        # Extract Author
        # <dt class="author">von <a class="username" href="./memberlist.php?mode=viewprofile&amp;u=_user_id_&amp
        #  ;sid=_sid_">_author_</a></dt>

        # class is either username or username-coloured
        author_soup = search_post_soup.find(
            "a", {"class": re.compile("^(username)")})
        author_info = ["Author", author_soup.text.strip(),
                       author_soup.get('href').strip()]
        single_post_data.append(author_info)
        if debug == True:
            print("   author:", author_info)

        attributes_soup = search_post_soup.findAll('dd')
        if debug == True:
            print("--------ATTRIBUTES--------")

        # convert attributes / special case for date
        for attribute_soup in attributes_soup:

            # Extract & Convert Date
            # <dd class="search-result-date">Montag 15. April 2019, 19:55</dd>
            try:
                if attribute_soup["class"][0] == "search-result-date":
                    date_string = attribute_soup.text.strip()
                    try:
                        # Convert Dates of sort Sonntag 9. Juni 2019, 09:00
                        date = datetime.strptime(
                            date_string, '%A %d. %B %Y, %H:%M')
                    except:
                        date = datetime(1900, 1, 1)
                    date_info = ["Datum", date, None]
                    single_post_data.append(date_info)
                    if debug == True:
                        print("   date_string:", date_string,
                              " datetime:", date_info)
                    continue
            except:
                pass

            # Extract other attributes according to  structure
            # <dd>_KEY_: <a href="./viewtopic.php?f=3&amp;t=_TOPIC_&amp;
            # hilit=_SEARCH_TERM_&amp;sid=_SID_">_VALUE_</a></dd>
            # extract link
            link = attribute_soup.find('a')
            if link is not None:
                link = link.get('href').strip()
            attributes = attribute_soup.text.split(':')
            attributes = list(map(str.strip, attributes))

            if len(attributes) == 2:
                # convert attribute to int if applicable
                try:
                    attributes[1] = int(attributes[1])
                except:
                    attributes[1] = attributes[1].encode(
                        'iso-8859-1', 'ignore').decode('utf8', 'ignore')
                attributes.append(link)
                single_post_data.append(attributes)
                if debug == True:
                    print("   attribute:", attributes)

        # extract text body / somehow the decoding doesn't work
        body_soup = search_post_soup.find("div", {"class": "postbody"})
        body = body_soup.text
        body = body.replace('\n', ' ').strip()

        text = ["Text", body, None]
        single_post_data.append(text)

        post_as_dict = [post_info_as_dict(attribute)
                        for attribute in single_post_data]
        post_as_json = json.dumps(post_as_dict, indent=4, sort_keys=True, default=str,ensure_ascii=False)
        post_data_json.append(post_as_json)     

        if debug == True:
            print("--------TEXT--------")
            print("   text:", text)
            print("########## OUTPUT DICT ############")
            print(post_as_dict)

    return post_data_json


def get_topics_from_soup(soup, debug=False, show_soup=False):
    """ transforms phpbb search results (topics/header only) as soup objects into list of dict objects
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
    """

    # post content of each found post
    post_data_json = []

    if soup is None:
        return post_data_json

    # extract all blocks enclosed by search post bg (followed by a number, therefore using regex)
    search_rows_soup = soup.findAll("li", {"class": re.compile("^(row bg)")})
    if debug is True:
        print("---------------------")
        print("Num Topics found:", len(search_rows_soup))

    if debug is True:
        show_info = True
    else:
        show_info = False
        
    for search_row_soup in search_rows_soup:

        if show_info == True:
            print("------------POST RESULT (only 1st is shown)-------------")
        post_as_dict = []
        # LAST POSTS
        # <dfn>Letzter Beitrag </dfn>von
        # <a href="./memberlist.php?mode=viewprofile..." class="username">...</a>
        # <a href="./viewtopic.php?f=9&amp;t=..." title="Gehe zum letzten Beitrag">
        # ...
        # </a>
        # <br />... date ...
        last_post_soup = search_row_soup.find("dd", {"class": "lastpost"})
        # last link
        latest_post_links = last_post_soup.findAll("a")
        if len(latest_post_links) >= 1:
            latest_post_link = get_link_data_from_soup(
                latest_post_links[-1])[0]
        else:
            latest_post_link = None

        # post Title and Links
        # <a class="topictitle" href="https://...">_text_</a>
        title_soup = search_row_soup.find("a", {"class": "topictitle"})
        if title_soup is not None:
            #post_link, post_text = get_link_data_from_soup(title_soup)
            post_text = get_link_data_from_soup(title_soup)[1]
            post_as_dict.append({"Thema": post_text, "link": latest_post_link})
            if show_info == True:
                print("POST TITLE", post_text)
                print("LATEST POST LINK", latest_post_link)
        # <dd class="posts">9999 <dfn>Antworten</dfn></dd>
        num_replies = int((search_row_soup.find(
            "dd", {"class": "posts"}).text).split()[0])
        # <dd class="views">9999 <dfn>Zugriffe</dfn></dd>
        num_views = int((search_row_soup.find(
            "dd", {"class": "views"}).text).split()[0])
        if show_info == True:
            print("NUM REPLIES, NUM VIEW:", num_replies, num_views)
        post_as_dict.append({"Antworten": num_replies, "link": None})
        post_as_dict.append({"Zugriffe": num_views, "link": None})

        # Thread Starter and Forum
        # <div class="responsive-hide left-box">
        # <i class="..." aria-hidden="true"></i>
        # von <a href="./memberlist.php?..." class="username">...</a>
        # &raquo; Mittwoch 15. November 2015, 20:00 &raquo;
        # in <a href="./viewforum.php?...">...</a>
        # </div>
        thread_start_soup = search_row_soup.find(
            "div", {"class": re.compile("^(responsive-hide)")})
        # thread start date is contained in 'xBB' unicode character ('>>'), extract inner string
        double_arrow = u'\xBB'
        search_pattern = double_arrow + '(.*)' + double_arrow
        #thread_start_date_str = re.search('>>(.*)>>', thread_start_soup.text).group(0)
        thread_start_date_str = re.search(
            search_pattern, thread_start_soup.text).group(1)
        thread_start_datetime = None
        if thread_start_date_str is not None:
            thread_start_date_str = thread_start_date_str.strip()
            thread_start_datetime = convert_datetime(thread_start_date_str)
            if show_info == True:
                print("Thread Start Date", thread_start_datetime)
            post_as_dict.append({"Datum": thread_start_datetime, "link": None})
        # get thread starter (contained in 1st link)
        user_soup = thread_start_soup.find("a", {'class':['username', 'username-coloured']})     
        
        if user_soup is not None:
            user_id, user_name = get_link_data_from_soup(user_soup)
            post_as_dict.append({"Author": user_name, "link": user_id})
            if show_info == True:
                print("USER", user_id, user_name)
        else:
            user_name = None
            user_soup_alt = thread_start_soup.find("span", {'class':'username'})     
            if user_soup_alt is not None:
                user_name = user_soup_alt.text         
            post_as_dict.append({"Author": user_name, "link": None})

       # <a class="username" href="...">...</a>
        last_user_soup = last_post_soup.find("a", {"class": "username"})             
        
        if last_user_soup is not None:
            last_user_id, last_user_name = get_link_data_from_soup(
                last_user_soup)
            post_as_dict.append(
                {"Author_Aenderung": last_user_name, "link": last_user_id})
            if show_info == True:
                print("LAST USER", last_user_id, last_user_name)            
        else:
            last_user_id = None
            last_user_name = None
            
            if last_post_soup is not None:
                # cases occurs that last user soup is None, try to extract it from last post soup
                # span class username for deleted members
                # span class username coloured for other members
                uname_colored_soup = last_post_soup.find("a", {"class": "username-coloured"})                
                uname_simple_soup = last_post_soup.find("span", {"class": "username"})         

                if uname_simple_soup is not None:
                    last_user_name = uname_simple_soup.text.strip()
                elif uname_colored_soup is not None:
                     last_user_id, last_user_name = get_link_data_from_soup(uname_colored_soup)                                     
                else:
                    pass
                                   
            post_as_dict.append({"Author_Aenderung": last_user_name, "link": last_user_id})


        last_post_soup_as_str = str(last_post_soup)
        # search for <br> sign in a dedicated row
        last_post_date_string = re.search(
            r'<br\/>.*\n', last_post_soup_as_str).group(0)[5:]
        last_post_datetime = convert_datetime(last_post_date_string)
        post_as_dict.append(
            {"Datum_Aenderung": last_post_datetime, "link": None})
        if show_info == True:
            print("LAST POST DATE TIME", str(last_post_datetime))

        # <div class="responsive-show" style="display: none;">
        #     Letzter Beitrag von <a href="./memberlist.php?mode=viewprofile&amp;u=..." class="username">...</a>
        # <a href="./viewtopic.php?f=9&amp;t=...&amp;hilit=...;p=..." title="Gehe zum letzten Beitrag">...</a>
        # <br />Verfasst in <a href="./viewforum.php?f=...">...</a>
        # </div>
        responsive_show_soup = search_row_soup.find(
            "div", {"class": "responsive-show"})

        # forum info is contained in last link
        forum_link_soup = responsive_show_soup.findAll("a")[-1]
        forum_id, forum_name = get_link_data_from_soup(forum_link_soup)
        if show_info == True:
            print("FORUM LINK,FORUM TITLE", forum_id, forum_name)
        post_as_dict.append({"Forum": forum_name, "link": forum_id})
        if show_info == True:
            print("- DICT RESULT--------------------")
            print(post_as_dict)
            print("---------------------------------")
        if show_soup == True:
            print("***   SOUP FOR ONE RESULT *****************")
            print(search_row_soup)
            print("*******************************************")
        post_as_json = json.dumps(
            post_as_dict, indent=4, sort_keys=True, default=str,ensure_ascii=False)
        post_data_json.append(post_as_json)
        show_info = False # Only show 1st post

    return post_data_json


def get_author_meta_from_soup(soup, debug=False, show_soup=False):
    """ transforms header columns of author list into dictionary
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
    """

    author_attributes = []
    soup_table_header = soup.find("thead")
    if soup_table_header is None:
        if debug is True:
            print("No Table Header found")
        return author_attributes

    soup_table_columns = soup_table_header.findAll("th")
    if show_soup is True:
        print("----TABLE COLUMNS AS SOUP----")
        print(soup_table_columns)

    for soup_table_column in soup_table_columns:
        author_column_attributes = {}
        table_column_class = soup_table_column.attrs['class'][0]
        soup_table_column_link = soup_table_column.find("a")
        if soup_table_column_link is not None:
            table_column_link = soup_table_column_link.attrs['href']
        else:
            table_column_link = None
        author_column_attributes["class"] = table_column_class
        author_column_attributes["link"] = table_column_link
        author_column_attributes["text"] = soup_table_column.text
        author_attributes.append(author_column_attributes)
        if debug is True:
            print("--------Author Column Info--------------")
            print("CLASS ", table_column_class)
            print("LINK ", table_column_link)
            print("TEXT", soup_table_column.text)
            # print(author_attributes)

    return author_attributes

def get_author_ref_from_soup(soup, debug=False, show_soup=False):
    """ transforms phpbb search results of author reference attributes into list of dictionary objects
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
    """
    
    authors_info = []
    soup_authors_info = soup.findAll("tr", {"class": re.compile("^(bg)")})
    if soup_authors_info is None:
        return authors_info
    if debug is True:
        print(f"Number of authors found: {len(soup_authors_info)}")
    for soup_author_info in soup_authors_info:
        author_info = {}
        if debug is True:
            print("---USER INFO---------")
        soup_username = soup_author_info.find("a", {"class": "username"})
        username = soup_username.text
        if 'href' in soup_username.attrs:
            user_profile = soup_username.attrs['href']
        else:
            user_profile = None

        soup_num_posts = soup_author_info.find("td", {"class": "posts"})
        num_posts = int(soup_num_posts.text)
        soup_homepage = soup_author_info.find("a", {"class": "postlink"})
        homepage = None
        if (soup_homepage is not None) and ('href' in soup_homepage.attrs):
            homepage = soup_homepage.attrs['href']

        date_registration_s = soup_author_info.findAll("td")[3].text
        date_registration = convert_datetime(date_registration_s)
        if show_soup is True:
            print("---------Soup--------------")
            print(f"Soup Username {soup_username}")
            print(f"Soup Posts {soup_num_posts}")
            print(f"Soup Homepage {soup_homepage}")
            print(f"Date Registration {date_registration}")
        if debug is True:
            print(
                f"Username: {username}/({user_profile}) registered on {date_registration}")
            print(f"Number of Posts {num_posts} Homepage:{homepage}")
            pass
        author_info["username"] = username
        author_info["user_profile"] = user_profile
        author_info["date_registration"] = date_registration
        author_info["num_posts"] = num_posts
        author_info["homepage"] = homepage
        authors_info.append(author_info)
    return authors_info

def soup_has_ajax_error(soup):
    """checks if soup contains attributes containing data-ajax error"""

    soup_divs = soup.findAll("div") 
    has_errors = False
    for soup_div in soup_divs:
    #   filter out all attributes starting with data-ajax
        if 'data-ajax-error-title' in soup_div.attrs:
            attributes_dict = soup_div.attrs
            regex = re.compile('^data-ajax')
            ajax_error_attributes = list(filter(regex.search,list(attributes_dict.keys())))
            print("--------AJAX ERROR OCCURED ACCESSING WEBSITE-----")
            [print(f"{ajax_attribute} : {attributes_dict[ajax_attribute]}") for ajax_attribute in ajax_error_attributes]
            print("--------------------------------------------------")               
            has_errors = True
    return has_errors  

def is_logged_in(soup):
    """ checks from code snippet whether user is logged in
        phpbb signatures
        Not Logged in 
        <a href="./ucp.php?mode=login" title="Anmelden" accesskey="x" role="menuitem">
            <i class="icon fa-power-off fa-fw" aria-hidden="true"></i><span>_log on message_</span>
        </a>
        Logged in 
        <a accesskey="x" href="./ucp.php?mode=logout&amp;sid=__sid__" role="menuitem" title="log off message">
        <i aria-hidden="true" class="icon fa-power-off fa-fw"></i><span>_log off message_</span>
        </a>    
    """
    logged_in = False
    login_link = soup.findAll("a",{"accesskey":"x"})
    if len(login_link) > 0:     
        link = login_link[0].attrs['href']        
        if link.find("logout") > 0:
            logged_in = True
    return logged_in 

def replace_relative_links(soup,base_url,debug=False):
    """ replaces relative link occurences starting with './' by base url """
    # only extract hyperlinks with href atributte
    if soup is None:
        return None

    links = soup.findAll('a', {"href" : True})
    links_replaced = 0
    for link in links:        
        url = link['href']
        if url.startswith("./"):
            link['href'] = base_url + url[1:len(url)]     
            links_replaced += 1
    if debug is True:
        print(f"soup_converter.replace_relative_links: {links_replaced} links replaced")
    return soup


