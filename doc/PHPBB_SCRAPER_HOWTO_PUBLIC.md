
# Test Code for phpBB Scraper <a name="00"></a>

* [(01) Testing Query Parameter Generation](#01)
* [(02) Create different phpBB URLs](#02)
* [(03) Test reading different html files](#03)
* [(04) Testing Request Module](#04)
* [(05) Testing Web Scraping](#05)
* [(06) Read json file and transform to dictionary](#06)
* [(07) Create HTML Table  and save it to file](#07)
* [(08) Read HTML file as soup, create filename, save as json, read json as dictionary, convert to HTML table and save HTML file](#08)
* [(09) Read Credentials and URL Base from Config file, initialize session and scraper, read one page, save data](#09)
* [(10) Read HTML file names from directory, read single html file](#10)
* [(11) Generate Query URL, create URL iterator to call URLs with indices](#11)
* [(12) Read Configuration, execute query, copy result to soup, replace relative by absolute links in soup](#12)
* [(13) Create Filename, Save soup as data string](#13)
* [(14) Convert soup as json entries, save it to file](#14)
* [(15) Read Snippet for Number of Topics in Soup](#15)
* [(16) Read JSON file, convert to dictionary, export as HTML file](#16)
  

# (01) Testing Query Parameter Generation <a name="01"></a>
[BACK](#00)


```python
from phpbb_scraper import persistence

# read user, password, url base from json file
config_file = r"C:\<path_to>\config.json"
config = persistence.read_json(filename=config_file)
user = config['user']
password = config['password']
base = config['base']
#print(f"base {base} user {user} password {password} base {base}")
debug = False
wait_time = 4
```

# (02) Create different phpBB URLs <a name="02"></a>
[BACK](#00)


```python
import imp
from phpbb_scraper import url_generator
from phpbb_scraper.url_generator import PhpbbUrlGenerator

dir(PhpbbUrlGenerator)
imp.reload(url_generator)
dir(PhpbbUrlGenerator)

url_gen = PhpbbUrlGenerator(base=base,debug=True)

# Hint Check Variable definition in source code
sort_by_creation_date = url_gen.get_query_param('SORT_BY_CREATION_DATE')
sort_by_forum = url_gen.get_query_param('SORT_BY_FORUM')
sort_descending = url_gen.get_query_param('SORT_DESCENDING')
sort_by_rank = url_gen.get_query_param('SORT_BY_RANK')
display_posts = url_gen.get_query_param('DISPLAY_POSTS')

print("Possible Query Parameters and url params",url_gen.QUERY_PARAMS_DICT)
print("----------------------")

start = 20
query = "test"

search_posts_desc_bydate = url_gen.get_query_url(query=query,sort_by=sort_by_creation_date,
                                             sort_order=sort_descending,search_result=display_posts,start=20)
print("search descending by date, posts",search_posts_desc_bydate)
display_topics = url_gen.get_query_param('DISPLAY_TOPICS')
# only search in title
search_type = url_gen.get_query_param('SEARCH_TITLE')
search_topics_desc_bydate = url_gen.get_query_url(query=query,sort_by=sort_by_forum,
                                             sort_order=sort_descending,search_type=search_type,
                                             search_result=display_topics,start=20)
print("search descending by date, topics",search_topics_desc_bydate)

# url for member list
member_list = url_gen.get_query_url(start=200,sort_by=sort_by_rank,member_list=True)
print("member list:",member_list)

# url for latest topics
active_topics =  url_gen.get_query_url(start=90,active_topics=True)
print("active topics:",active_topics)


```

# (03) Test reading different html files <a name="03"></a>
[BACK](#00)


```python
import imp
from phpbb_scraper import persistence
from phpbb_scraper import soup_converter
from phpbb_scraper import url_generator
from phpbb_scraper.url_generator import PhpbbUrlGenerator

imp.reload(url_generator)
imp.reload(persistence)
imp.reload(soup_converter)

file_test = r"C:\C:\<path_to>\test.txt"
file_test_copy = r"C:\<path_to>\test_copy.txt"
file_phpbb_topics = r"C:\<path_to>\PAGE_TopicsOnly.html"
file_phpbb_posts = r"C:\<path_to>\PAGE_TopicsAndTexts.html"
file_phpbb_team_member = r"C:\<path_to>\PAGE_TeamMembers.html"
file_phpbb_member_profile = r"C:\<path_to>\PAGE_MemberProfilePage.html"
file_phpbb_active = r"C:\<path_to>\PAGE_ActiveTopics.html"
file_phpbb_timeout = r"C:\<path_to>\PAGE__timeout.html"
file_phpbb_no_log_in = r"C:\<path_to>\PAGE_NoLogin.html"
file_phpbb_json_orig = r"C:\<path_to>\test_orig.json"
file_phpbb_json_copy = r"C:\<path_to>\test_copy.json"

print("##### testing persistence module #######")
# testing copy and paste
persistence.copy_file(source=file_test,target=file_test_copy,force_delete=True)
# testing reading and writing of json file
persistence.copy_file(source=file_phpbb_json_orig,target=file_phpbb_json_copy,force_delete=True)
# testing json methods
print("---data from json---")
data_from_json = persistence.read_json(file_phpbb_json_copy,debug=False)
#data_from_json = *data_from_json
print(len(data_from_json))
print("---appending data---")
persistence.append_json(file_phpbb_json_copy,data_from_json,debug=True)
print("---reading data again---")
data_from_json_2 = persistence.read_json(file_phpbb_json_copy,debug=True)
print(data_from_json_2)
print("##### testing  #######")

print("+++ loading test files +++")
soup_timeout =  soup_converter.read_soup(file_phpbb_timeout,debug=True)
soup_active =  soup_converter.read_soup(file_phpbb_active,debug=True)
soup_no_log_in = soup_converter.read_soup(file_phpbb_no_log_in,debug=True)

print("+++ read soup information +++")
soup_posts =  soup_converter.read_soup(file_phpbb_posts,debug=False)
post_results = soup_converter.get_posts_from_soup(soup_posts,debug=False,show_soup=False)
print("Post Results read:",len(post_results))
soup_topics =  soup_converter.read_soup(file_phpbb_topics,debug=False)
topic_results = soup_converter.get_topics_from_soup(soup_topics,debug=False,show_soup=False)
print("Post Topics read:",len(topic_results))
soup_team_member =  soup_converter.read_soup(file_phpbb_team_member,debug=False)
member_results = soup_converter.get_author_ref_from_soup(soup_team_member,debug=False,show_soup=False)
print("Members Counted:",len(member_results))
#soup_member_profile =  soup_converter.read_soup(file_phpbb_member_profile,debug=False)
#print(soup_member_profile)
# ????
member_profile = soup_converter.get_author_meta_from_soup(soup_team_member,debug=False,show_soup=True)
print("Member Profile", member_profile)

```

# (04) Testing Request Module <a name="04"></a>
[BACK](#00)


```python
import imp
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
import phpbb_scraper.persistence as persistence
imp.reload(scraper)

# read user, password, url base from json file
config_file = r"C:\<path_to>\config.json"
config = persistence.read_json(filename=config_file)
user = config['user']
password = config['password']
base = config['base']
print(f"base {base} user {user} password {password} base {base}")
debug = False
wait_time = 4

scraper = PhpbbScraper(base=base,debug=debug,wait_time=wait_time,user=user,password=password)
print(f"Scraper URL LogIn: {scraper.get_login_url()}")
s = scraper.get_session()
print(f"Session Cookies: {s.cookies}")
s.close()
```

# (05) Testing Web Scraping <a name="05"></a>
[BACK](#00)


```python
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
from phpbb_scraper import soup_converter
from phpbb_scraper import html_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
import phpbb_scraper.persistence as persistence

import traceback
import imp
from datetime import datetime
imp.reload(scraper)
imp.reload(html_converter)
imp.reload(soup_converter)
imp.reload(persistence)

# master data / setup
credential_file = r"C:\<path_to>\credentials.json"
user_login_data = persistence.read_json(filename=credential_file)
username = user_login_data['user']
password = user_login_data['password']
base = config['base']
debug = False
wait_time = 4

# search term
query = r"offen"
# start index
start = 0

# construct the url
# Hint Check Variable definition in source code
url_gen = PhpbbUrlGenerator(base=base,debug=debug)

# all defined contant values to create specific query parts
SEARCH_PAST_DAYS = url_gen.get_query_param('SEARCH_PAST_DAYS')
SEARCH_PAST_7DAYS = url_gen.get_query_param('SEARCH_PAST_7DAYS')
SORT_BY_FORUM = url_gen.get_query_param('SORT_BY_FORUM')
SORT_BY_AUTHOR = url_gen.get_query_param('SORT_BY_AUTHOR') 
SORT_BY_CREATION_DATE = url_gen.get_query_param('SORT_BY_CREATION_DATE')
SORT_BY_TOPIC = url_gen.get_query_param('SORT_BY_TOPIC') 
SORT_BY_POST = url_gen.get_query_param('SORT_BY_POST') 
SORT_BY_RANK = url_gen.get_query_param('SORT_BY_RANK') 
SORT_BY_REGISTRATION = url_gen.get_query_param('SORT_BY_REGISTRATION') 
SORT_ASCENDING = url_gen.get_query_param('SORT_ASCENDING')
SORT_DESCENDING = url_gen.get_query_param('SORT_DESCENDING') 
SEARCH_ALL = url_gen.get_query_param('SEARCH_ALL') 
SEARCH_TOPIC = url_gen.get_query_param('SEARCH_TOPIC')
SEARCH_TITLE = url_gen.get_query_param('SEARCH_TITLE')
SEARCH_FIRST_POST = url_gen.get_query_param('SEARCH_FIRST_POST')
SEARCH_FORUM_ONLY = url_gen.get_query_param('SEARCH_FORUM_ONLY')
SEARCH_SUBFORUM = url_gen.get_query_param('SEARCH_SUBFORUM')
DISPLAY_TOPICS = url_gen.get_query_param('DISPLAY_TOPICS')
DISPLAY_POSTS = url_gen.get_query_param('DISPLAY_POSTS')
DISPLAY_NUM_CHARACTERS = url_gen.get_query_param('DISPLAY_NUM_CHARACTERS')
KEYWORDS = url_gen.get_query_param('KEYWORDS')
TERMS_ANY = url_gen.get_query_param('TERMS_ANY')
TERMS_ALL = url_gen.get_query_param('TERMS_ALL')
AUTHOR = url_gen.get_query_param('AUTHOR')
START_POSITION = url_gen.get_query_param('START_POSITION')
ACTIVE_TOPICS = url_gen.get_query_param('ACTIVE_TOPICS')  

# search title, output list of titles
url_search_title_desc_bydate = url_gen.get_query_url(query=query,sort_by=SORT_BY_CREATION_DATE,
                                                     sort_order=SORT_DESCENDING,search_result=DISPLAY_TOPICS,
                                                     terms=TERMS_ALL,search_type=SEARCH_TITLE,start=start)
print("search descending by date, topics",url_search_title_desc_bydate)
scrape_url = url_search_title_desc_bydate
scraper = PhpbbScraper(base=base,debug=debug,wait_time=wait_time,user=user,password=password)
```

# (06) Read json file and transform to dictionary <a name="06"></a>
[BACK](#00)


```python
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
from phpbb_scraper import html_converter
from phpbb_scraper import soup_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
import phpbb_scraper.persistence as persistence
import traceback
import imp
import json
from datetime import datetime
imp.reload(scraper)
imp.reload(html_converter)
imp.reload(soup_converter)
imp.reload(persistence)

f = r"C:\<path_to>\test.json"
data = persistence.read_json(f)
print(f"Num Entries in file {f}: {len(data)}")
json_string = data[0]

d = persistence.read_json_as_dict(filename=f,debug=True)
print(d[1]["Thema"]["link"])


```

# (07) Create HTML Table  and save it to file <a name="07"></a>
[BACK](#00)


```python
import imp
from phpbb_scraper import persistence
from phpbb_scraper import html_converter
imp.reload(persistence)
imp.reload(html_converter)
data = "string2"
path = r"C:<path_to>"
filename = r"test"
file_ext = "txt"
append_tst = True
#persistence.save_data(data,filename,path=path,file_extension=file_ext,append_timestamp=True)

#a=["test"]
#type(a) is list
url = "http://test_page"
linktext = "link"
link = html_converter.link(link=url,text=linktext)
test_table = [["a",link],["c",link],["e",link]]
              
test_html = html_converter.get_html_table(test_table)
persistence.save_data(test_html,filename,path=path,file_extension="html",append_timestamp=True)
print(test_html)
               

```

# (08) Read HTML file as soup, create filename, save as json, read json as dictionary, convert to HTML table and save HTML file <a name="08"></a>
[BACK](#00)


```python
# read html file with posts and transform it as json file and back as dictionary
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
from phpbb_scraper import html_converter
from phpbb_scraper import soup_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
import phpbb_scraper.persistence as persistence
import traceback
import imp
import json
from datetime import datetime
imp.reload(scraper)
imp.reload(html_converter)
imp.reload(soup_converter)
imp.reload(persistence)

p_html = r"C:\<path_to>\test_posts.html"
p_soup = soup_converter.read_soup(url=p_html)
p = soup_converter.get_posts_from_soup(p_soup)
#print(f"type {type(p[0])} {p[0]}")
print("----------------------------------")
t_html = r"C:\<path_to>\test_topics.html"
t_soup = soup_converter.read_soup(url=t_html)
t = soup_converter.get_topics_from_soup(t_soup)
#print(f"type {type(t[0])} {t[0]}")
print("----------------------------------")
d = r"C:\<path_to>\Desktop"
f = r"test_posts"
filename = persistence.create_filename(f,path=d,file_extension="json",append_timestamp=False)
print(filename)
persistence.append_json(filename=filename,dict_entries=p)
print(f"done, written on file {filename}")
f = r"test_topics"
filename = persistence.create_filename(f,path=d,file_extension="json",append_timestamp=False)
persistence.append_json(filename=filename,dict_entries=t)
print(f"done, written on file {filename}")
f_p = r"C:\<path_to>\test_posts.json"
f_t = r"C:\<path_to>\test_topics.json"
#data = persistence.read_json(f)
data_t  = persistence.read_json_as_dict(f_t)
html_t = html_converter.dict_as_html(data_t)


print(f"TOPICS type {type(data_t[0])} \n {data_t[0]}")
print(f"Num Entries in file {f}: {len(data_t)}")
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
data_p  = persistence.read_json_as_dict(f_p)
html_p = html_converter.dict_as_html(data_p)
print(f"POSTS type {type(data_p[0])} \n {data_p[0]}")
print(f"Num Entries in file {f}: {len(data_p)}")
####################
#def save_data(data,filename,path=None,file_extension=None,append_timestamp=True):
ft = r"test_topics"
fp = r"test_posts"
e = "html"
persistence.save_data(html_p,fp,path=d,file_extension=e,append_timestamp=False)
persistence.save_data(html_t,ft,path=d,file_extension=e,append_timestamp=False)
```

# (09) Read Credentials and URL Base from Config file, initialize session and scraper, read one page, save data   <a name="09"></a>
[BACK](#00)


```python
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
from phpbb_scraper import soup_converter
from phpbb_scraper import html_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
import phpbb_scraper.persistence as persistence

import traceback
import imp
from datetime import datetime
imp.reload(scraper)
imp.reload(html_converter)
imp.reload(soup_converter)
imp.reload(persistence)

# read user, password, url base from json file
config_file = r"C:\3<path_to>\config.json"
config = persistence.read_json(filename=config_file)
user = config['user']
password = config['password']
base = config['base']
debug = False
wait_time = 5
scraper = PhpbbScraper(base=base,debug=debug,wait_time=wait_time,user=user,password=password)
#print(f"base {base} user {user} password {password} base {base}")

url = r"https://<forum>"
print(url)
p = r"C:\<path_to>\Desktop"
fu = r"test_utf8"
f8 = r"test_8859"
iso_encode = 'iso-8859-1'
rf = r"C:\<path_to>\test_utf8.html"
try:
    sess = scraper.get_session()
    soup = scraper.get_data(session=sess,url=url)    
#def save_data(data,filename,path=None,file_extension=None,append_timestamp=True,encoding='utf-8'):    
    persistence.save_data(str(soup),fu,path=p,file_extension="html",append_timestamp=False)
    #persistence.save_data(str(soup),f8,path=p,file_extension="html",append_timestamp=False,encoding=iso_encode)
    #print(soup)
    sess.close()    
except:    
    print(traceback.format_exc())
soup_read = soup_converter.read_soup(rf)    
print(soup_read)
print("end")


```

# (10) Read HTML file names from directory, read single html file <a name="10"></a>
[BACK](#00)


```python
d = r"C:\<path_to>"
file_name =  persistence.read_html_file_names(d)[0]
print(file_name)
soup_read = soup_converter.read_soup(file_name)
print(soup_read)
```

# (11) Generate Query URL, create URL iterator to call URLs with indices <a name="11"></a>
[BACK](#00)


```python
from phpbb_scraper.scraper import PhpbbScraper
from phpbb_scraper import scraper
from phpbb_scraper import soup_converter
from phpbb_scraper import html_converter
from phpbb_scraper.url_generator import PhpbbUrlGenerator
import phpbb_scraper.persistence as persistence

import traceback
import imp
from datetime import datetime
imp.reload(scraper)
imp.reload(html_converter)
imp.reload(soup_converter)
imp.reload(persistence)

start_index = 0
increment = 70
num_steps = 4
end_index = start_index + num_steps*increment
#print(end_index)
r = list(range(start_index,end_index,increment))

url_gen = PhpbbUrlGenerator(base="http://<forum>",debug=False)

# Hint Check Variable definition in source code
sort_by_creation_date = url_gen.get_query_param('SORT_BY_CREATION_DATE')
sort_by_forum = url_gen.get_query_param('SORT_BY_FORUM')
sort_descending = url_gen.get_query_param('SORT_DESCENDING')
sort_by_rank = url_gen.get_query_param('SORT_BY_RANK')
display_posts = url_gen.get_query_param('DISPLAY_POSTS')

#print("Possible Query Parameters and url params",url_gen.QUERY_PARAMS_DICT)
#print("----------------------")

start = 20
query = "offen test"

search_posts_desc_bydate = url_gen.get_query_url(query=query,sort_by=sort_by_creation_date,
                                             sort_order=sort_descending,search_result=display_posts,start=0)

query_it = url_gen.get_query_url_iterator(query=query,sort_by=sort_by_creation_date,
                                          sort_order=sort_descending,search_result=display_posts,
                                          start=15,num_steps=3,increment=15)

for query in query_it:
    print(query)
```

# (12) Read Configuration, execute query, copy result to soup, replace relative by absolute links in soup <a name="12"></a>
[BACK](#00)


```python
from phpbb_scraper.url_generator import PhpbbUrlGenerator
from phpbb_scraper import scraper
from phpbb_scraper.scraper import ScraperExecutor
from phpbb_scraper import soup_converter
import imp
#PhpbbUrlGenerator.QUERY_PARAMS_DICT
imp.reload(scraper)
config_file = r"C:\<path_to>\config.json"
target_dir = r"C:\<path_to>\TEST"
executor = ScraperExecutor(config_file=config_file,target_dir=target_dir)
base_url = executor.base_url
DISPLAY_TOPICS = executor.QUERIES['DISPLAY_TOPICS']
url_gen = PhpbbUrlGenerator(base=base_url)
#print(executor.QUERIES)
# build url for latest posts
#   def get_query_url(cls,query=None,base=None,sort_by=None,sort_order=None,
#                      search_type=None,search_forum=None,search_result=None,num_chars=None,
#                      terms=None,author=None,start=None,member_list=False,active_topics=False):
url_latest_topics = url_gen.get_query_url(active_topics=True)
print(url_latest_topics)
soup = executor.get_soup(url_latest_topics)
print(f"soup was read, length {len(str(soup))}")
# replace relative links by absolute path
soup = soup_converter.replace_relative_links(soup,base_url)

```

# (13) Create Filename, Save soup as data string <a name="13"></a>
[BACK](#00)


```python
from phpbb_scraper import persistence
import imp
imp.reload(persistence)
name = r"test_active_topics"
path = r"C:\<path_to>\TEST"
extension = "html"
append_timestamp = False
filename = persistence.create_filename(name,path=path,file_extension=extension,append_timestamp=append_timestamp)
print(filename)
persistence.save_data(str(soup),filename)
```

# (14) Convert soup as json entries, save it to file <a name="14"></a>
[BACK](#00)


```python
from phpbb_scraper import soup_converter
from phpbb_scraper import persistence
import imp
imp.reload(persistence)
imp.reload(soup_converter)
#print(soup)
#soup_converter.get_search_result_data_from_soup(soup=soup,show_soup=True)
#soup
json_entries=soup_converter.get_topics_from_soup(soup,debug=False)
print((json_entries[0]))
name = r"test"
path = r"C:\<path_to>\TEST"
extension = "json"
append_timestamp = True
filename = persistence.create_filename(name,path=path,file_extension=extension,append_timestamp=append_timestamp)
print(filename)
#def create_filename(filename,path=None,file_extension=None,append_timestamp=True):
#str(soup)
persistence.append_json(filename, json_entries, debug=False)

```

# (15) Read Snippet for Number of Topics in Soup <a name="15"></a>
[BACK](#00)


```python
from phpbb_scraper import soup_converter
from phpbb_scraper import persistence
import re
imp.reload(persistence)
imp.reload(soup_converter)
testfile = r"C:\<path_to>\test_active_topics.html"
base = "###LINK###"
# def get_search_result_data_from_soup(soup, debug=False, show_soup=False) persistence
soup = soup_converter.read_soup(testfile,base_url=base,debug=True)
#soup_converter.get_search_result_data_from_soup(soup,show_soup=True)
#print(str(soup))
soup_converter.get_num_topics(soup)
# try:
#     num = int(re.search('Die Suche ergab (\d+) Treffer', str(soup)).group(1))
# except:
#     num = 0
# print(num) 

```

# (16) Read JSON file, convert to dictionary, export as HTML file <a name="16"></a>
[BACK](#00)


```python
import imp
from phpbb_scraper import persistence 
from phpbb_scraper import html_converter
#read json file
imp.reload(persistence)
json_file = r"C:\<path_to>\test.json"
html_file = r"C:\<path_to>\test_html.html"
json_data = persistence.read_json(json_file, debug=False)
print(json_data[0])
# transform each json entry
"""  {
        "<key>": "<value>",
        "link": "<link>"
       },
       into dictionary entry
       {<key>:{"value":<value>,"link":<link>}}
"""
json_as_dict = persistence.read_json_as_dict(json_file,debug=False)
#print(len(json_as_dict))
print("Sample Entry",json_as_dict[0])
print("keys",json_as_dict[0].keys())
#sample readout
key = "Thema"
dict_data = json_as_dict[0][key]
#print(f" key:{key},value {dict_data["value"]},link {dict_data["link"]}")
print(f"\n ( key:{key} \n value {dict_data['value']} \n link {dict_data['link']} )")
# export as HTML Table and Save
html = html_converter.dict_as_html(json_as_dict)
persistence.save_data(html,html_file)
print("file saved")


```
