
# PHPBB Scraping Data API - Sample Use
## Configuration
Here's a possible use for the phpbb Scraper API, that will read latest topics from a forum. Setup to access the forum is done in a config.json, that has the following content:
```
{
    "user": "<user>",
    "password": "<password>",
    "base":"https://<forum url>",
    "target_dir":"<target dir where to save / read html files",
    "meta_file":"<targetFileWhereToAppendHtmlMetaData>"    
}
    mind the double backslash and encoding:
    eg meta_file = "C:\\Users\\JohnDoe\\Desktop\\TEST\\metafile.json"
```
The ScraperExecutor encapsulates generation of URL, log in, reading and processing of scraped forum pages
 

## Code is Documented :-)


```python
import phpbb_scraper
from phpbb_scraper.scraper import ScraperExecutor
# code is documented, use help(<module>) to find out more about implemented code
# for inner structure, use dir(module)
help(ScraperExecutor)
```

    Help on class ScraperExecutor in module phpbb_scraper.scraper:
    
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
    
    

## Sample Scrape
The following sample shows application of the ScraperExecutor class that reads latest topics and saves them as HTML files and updates the meta file (list of files downloaded)


```python
from phpbb_scraper.scraper import ScraperExecutor

# config file  path
config_file = r"C:\<path>\config.json"

debug = False   # run in debug mode
steps_num = 2  # num of max web pages to be scraped

# set configuration and instanciate web scraper
executor = ScraperExecutor(config_file=config_file,debug=debug)
# scrapes data from forum , saves them to files and returns metadata of each scraped page
metadata = executor.retrieve_last_topics(steps_num=steps_num)

```

Display Of meta data for scraping of each Page: To make it unique, each scraped page (and forum posts later on, as well) gets hash ids alongside with file name so as to make it ready for analysis in subsequent steps 


```python
# in case everything went fine, you can see the file metadata here (=what is appended to the metadata file)
metadata
```




    [{'url': 'https://<forum>/search.php?st=14&sk=t&sd=d&sf=msgonly&search_id=active_topics&start=0&sr=topics',
      'url_hash': '5112ecd9d1501ef9cdb68320cce1206e',
      'soup_id': '20191125_213646_5112ecd9d1501ef9cdb68320cce1206e',
      'date': datetime.datetime(2019, 11, 25, 21, 36, 46, 347731),
      'key': 'bcae2fa43ba6e782c8bcf4a8f8c6e070',
      'filename': '20191125_213646_5112ecd9d1501ef9cdb68320cce1206e.html'},
     {'url': 'https://<forum>/search.php?st=14&sk=t&sd=d&sf=msgonly&search_id=active_topics&start=70&sr=topics',
      'url_hash': '0c994f9ce5110b358d7a0e38b65e11d2',
      'soup_id': '20191125_213646_0c994f9ce5110b358d7a0e38b65e11d2',
      'date': datetime.datetime(2019, 11, 25, 21, 36, 46, 347731),
      'key': '2f57d15d7f03dc46ce971c6a9bdaa86b',
      'filename': '20191125_213646_0c994f9ce5110b358d7a0e38b65e11d2.html'}]



## Reading Of Scraped Data
Read of scraped html data can be done with the read_topics_from_meta() function: It reads the metafile, accesses the referenced files there, and imports each post as dictionary.


```python
from phpbb_scraper.scraper import ScraperExecutor

# read the urls from metafile and get post data as dictionary from stored html files

config_file = r"C:\30_Entwicklung\WORK_JUPYTER\phpbb_scraper_html_sample\config.json"

# read the urls from metafile and get metadata from stored html files
debug = False   # run in debug mode

# set configuration
executor = ScraperExecutor(config_file=config_file,debug=debug)

# read metafile and access locally stored html files
topics = executor.read_topics_from_meta() #dictionary containing topics metadata
print(f"Number of topics {len(topics)}, type of topics: {type(topics)}")
print(f"Metadata Keys per Post: {list(topics[list(topics.keys())[0]].keys())}")
```

    Reading file C:\<path>\20191116_133454_5112ecd9d1501ef9cdb68320cce1206e.html
    Reading file C:\<path>\20191116_133454_0c994f9ce5110b358d7a0e38b65e11d2.html
    Reading file C:\<path>\20191125_213338_5112ecd9d1501ef9cdb68320cce1206e.html
    Reading file C:\<path>\20191125_213338_0c994f9ce5110b358d7a0e38b65e11d2.html
    Reading file C:\<path>\20191125_213646_5112ecd9d1501ef9cdb68320cce1206e.html
    Reading file C:\<path>\20191125_213646_0c994f9ce5110b358d7a0e38b65e11d2.html
    Number of topics 258, type of topics: <class 'dict'>
    Metadata Keys per Post: ['post_thema', 'post_thema_link', 'source_key', 'source_date', 'source_filename', 'source_soup_id', 'source_url', 'source_url_hash', 'post_antworten', 'post_zugriffe', 'post_datum', 'post_author', 'post_author_link', 'post_author_aenderung', 'post_author_aenderung_link', 'post_datum_aenderung', 'post_forum', 'post_forum_link']
    

Having transformed posts into dictionary, everything is set for further analysis :-)

## Scraped Data as HTML Table
ScraperExecutor method save_topics_as_html_table will read scraped data and is transforming them into tabular HTML data


```python
from phpbb_scraper.scraper import ScraperExecutor

config_file = r"C:\<path>\phpbb_scraper_html_sample\config.json"

# read the urls from metafile and get metadata from stored html files
debug = False   # run in debug mode

# set configuration
executor = ScraperExecutor(config_file=config_file,debug=debug)

# html file name and path
html_file = r"posts_as_html_table"
path = r"C:\<path>\TEST"
add_timestamp = False

# create html table from dictionary and save file locally
executor.save_topics_as_html_table(html_file=html_file,path=path,append_timestamp=add_timestamp)



```

    Reading file C:\<path>\20191116_133454_5112ecd9d1501ef9cdb68320cce1206e.html
    Reading file C:<path>\20191116_133454_0c994f9ce5110b358d7a0e38b65e11d2.html
    Reading file C:\<path>\20191125_213338_5112ecd9d1501ef9cdb68320cce1206e.html
    Reading file C:\<path>\20191125_213338_0c994f9ce5110b358d7a0e38b65e11d2.html
    Reading file C:\<path>\20191125_213646_5112ecd9d1501ef9cdb68320cce1206e.html
    Reading file C:\<path>\20191125_213646_0c994f9ce5110b358d7a0e38b65e11d2.html
    Data saved to C:\<path>\posts_as_html_table_20191125_213716.html
    
