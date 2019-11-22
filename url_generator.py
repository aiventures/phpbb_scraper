"""Class PhpbbUrlGenerator generates URL for reading phpbb web pages"""
# import required libs ...
import urllib.parse as urlparse

# Class for generating URL
class PhpbbUrlGenerator:
    """generates URL for reading phpbb web pages"""
    DEBUG = False
        
    #query param name constants
    QUERY_PARAM_DAYS = 'st'
    QUERY_PARAM_SORT_BY = 'sk'
    QUERY_PARAM_SORT_ORDER = 'sd'
    QUERY_PARAM_SEARCH_TYPE = 'sf'
    QUERY_PARAM_SEARCH_FORUM = 'sc'
    QUERY_PARAM_SEARCH_RESULT = 'sr'
    QUERY_PARAM_NUM_CHARS = 'ch'
    QUERY_PARAM_KEYWORDS = 'keywords'
    QUERY_PARAM_TERMS = 'terms'
    QUERY_PARAM_AUTHOR = 'author'
    QUERY_PARAM_START = 'start'      
    QUERY_PARAM_SEARCH_ID = 'search_id'
    
    #query url params
    SEARCH_PAST_DAYS = {QUERY_PARAM_DAYS:'0'}
    SEARCH_PAST_7DAYS = {QUERY_PARAM_DAYS:'7'}
    SORT_BY_FORUM = {QUERY_PARAM_SORT_BY:'f'}
    SORT_BY_AUTHOR = {QUERY_PARAM_SORT_BY:'a'}
    SORT_BY_CREATION_DATE = {QUERY_PARAM_SORT_BY:'t'}
    SORT_BY_TOPIC = {QUERY_PARAM_SORT_BY:'i'}
    SORT_BY_POST = {QUERY_PARAM_SORT_BY:'s'}
    SORT_BY_RANK = {QUERY_PARAM_SORT_BY:'m'}
    SORT_BY_REGISTRATION = {QUERY_PARAM_SORT_BY:'c'}
    SORT_ASCENDING = {QUERY_PARAM_SORT_ORDER:'a'}
    SORT_DESCENDING = {QUERY_PARAM_SORT_ORDER:'d'}
    SEARCH_ALL = {QUERY_PARAM_SEARCH_TYPE:'all'}
    SEARCH_TOPIC = {QUERY_PARAM_SEARCH_TYPE:'msgonly'}
    SEARCH_TITLE = {QUERY_PARAM_SEARCH_TYPE:'titleonly'}
    SEARCH_FIRST_POST = {QUERY_PARAM_SEARCH_TYPE:'firstpost'}
    SEARCH_FORUM_ONLY = {QUERY_PARAM_SEARCH_FORUM:'0'}
    SEARCH_SUBFORUM = {QUERY_PARAM_SEARCH_FORUM:'1'}
    DISPLAY_TOPICS =  {QUERY_PARAM_SEARCH_RESULT:'topics'}
    DISPLAY_POSTS =  {QUERY_PARAM_SEARCH_RESULT:'posts'}
    DISPLAY_NUM_CHARACTERS =  {QUERY_PARAM_NUM_CHARS:'200'}
    KEYWORDS =  {QUERY_PARAM_KEYWORDS:''}
    TERMS_ANY = {QUERY_PARAM_TERMS:'any'}  
    TERMS_ALL = {QUERY_PARAM_TERMS:'all'}  
    AUTHOR = {QUERY_PARAM_AUTHOR:''}
    START_POSITION = {QUERY_PARAM_START:'0'}  
    ACTIVE_TOPICS = {QUERY_PARAM_SEARCH_ID:'active_topics'} 
    
    #dict of query url params and keys
    QUERY_PARAMS_DICT = { 'SEARCH_PAST_DAYS':SEARCH_PAST_DAYS,
                          'SEARCH_PAST_7DAYS':SEARCH_PAST_7DAYS,
                          'SORT_BY_FORUM':SORT_BY_FORUM,
                          'SORT_BY_AUTHOR':SORT_BY_AUTHOR, 
                          'SORT_BY_CREATION_DATE':SORT_BY_CREATION_DATE,
                          'SORT_BY_TOPIC':SORT_BY_TOPIC, 
                          'SORT_BY_POST':SORT_BY_POST, 
                          'SORT_BY_RANK':SORT_BY_RANK, 
                          'SORT_BY_REGISTRATION':SORT_BY_REGISTRATION, 
                          'SORT_ASCENDING':SORT_ASCENDING,
                          'SORT_DESCENDING':SORT_DESCENDING, 
                          'SEARCH_ALL':SEARCH_ALL, 
                          'SEARCH_TOPIC':SEARCH_TOPIC,
                          'SEARCH_TITLE':SEARCH_TITLE,
                          'SEARCH_FIRST_POST':SEARCH_FIRST_POST,
                          'SEARCH_FORUM_ONLY':SEARCH_FORUM_ONLY,
                          'SEARCH_SUBFORUM':SEARCH_SUBFORUM,
                          'DISPLAY_TOPICS':DISPLAY_TOPICS,
                          'DISPLAY_POSTS':DISPLAY_POSTS,
                          'DISPLAY_NUM_CHARACTERS':DISPLAY_NUM_CHARACTERS,
                          'KEYWORDS':KEYWORDS,
                          'TERMS_ANY':TERMS_ANY,
                          'TERMS_ALL':TERMS_ALL,
                          'AUTHOR':AUTHOR,
                          'START_POSITION':START_POSITION,
                          'ACTIVE_TOPICS':ACTIVE_TOPICS }              
    
    # default param dictionary containing all default values
    DEFAULT_QUERY_PARAMS = {**SEARCH_PAST_DAYS,**SORT_BY_CREATION_DATE,
                            **SORT_DESCENDING,**SEARCH_ALL,**SEARCH_SUBFORUM,
                            **DISPLAY_TOPICS,**DISPLAY_NUM_CHARACTERS,
                            **KEYWORDS,**TERMS_ALL,**AUTHOR,**START_POSITION}   
              
    # query for active topics                  
    ACTIVE_TOPICS_QUERY_PARAMS = {**SEARCH_PAST_7DAYS,**SORT_BY_CREATION_DATE,
                                  **SORT_DESCENDING,**SEARCH_TOPIC,**ACTIVE_TOPICS,**START_POSITION}
    
    # query for member list  
    MEMBER_LIST_QUERY_PARAMS = {**SORT_BY_REGISTRATION,**SORT_DESCENDING,**START_POSITION}
                                          
    base_url = r"https://<base_url>"
    search_address = 'search.php'
    memberlist_address = 'memberlist.php'
              
    @classmethod                 
    def __init__(cls, base=None,debug=False):
        cls.DEBUG = debug
        if base is not None:
            cls.base_url = base
        if cls.DEBUG is True:
            print("Constructor, Base set to",base)
    
    @classmethod    
    def set_debug(cls,debug=True):    
        """activate debug info display"""
        
        cls.DEBUG = debug
                  
    @classmethod    
    def get_query_param(cls,query_param_key):    
        """ input one of query url params > output: dictionary value """
        
        value = None
        query_param = cls.QUERY_PARAMS_DICT.get(query_param_key)
        if query_param is not None:
          value = next(iter(query_param.values()))
        return value

    @classmethod    
    def set_base_url(cls,base_url):    
        """setting base url"""
        
        cls.base_url = base_url
        if cls.DEBUG is True:
            print("base url:",base_url)                    
        
    @classmethod
    def get_default_query_params(cls):    
        """ generate default settings for phpbb query parameters """
        
        return cls.DEFAULT_QUERY_PARAMS.copy()            
              
    # general search
    @classmethod    
    def get_query_url(cls,query=None,base=None,sort_by=None,sort_order=None,
                       search_type=None,search_forum=None,search_result=None,num_chars=None,
                       days=None,terms=None,author=None,start=None,member_list=False,
                       active_topics=False):
        """constructs final url for generating phpbb urls"""      
        
        if base is not None:
            cls.base_url = base
        
        query_url = urlparse.urljoin(cls.base_url,cls.search_address)+'?'      
              
        if member_list is True:
            query_url = urlparse.urljoin(cls.base_url,cls.memberlist_address)+'?'                          
            query_params = cls.MEMBER_LIST_QUERY_PARAMS.copy()  
        elif active_topics is True:
            query_params = cls.ACTIVE_TOPICS_QUERY_PARAMS.copy()  
        else:
            query_params = cls.DEFAULT_QUERY_PARAMS.copy()                                                                                                                
        
        # logic for update of query parameters (None=Ignore update otherwise)
        query_params_update = {cls.QUERY_PARAM_SORT_BY:sort_by,
                               cls.QUERY_PARAM_SORT_ORDER:sort_order,
                               cls.QUERY_PARAM_SEARCH_TYPE:search_type,
                               cls.QUERY_PARAM_SEARCH_FORUM:search_forum,
                               cls.QUERY_PARAM_SEARCH_RESULT:search_result,
                               cls.QUERY_PARAM_NUM_CHARS:num_chars,
                               cls.QUERY_PARAM_DAYS:days,
                               cls.QUERY_PARAM_TERMS:terms,
                               cls.QUERY_PARAM_AUTHOR:author,
                               cls.QUERY_PARAM_START:start}  
        query_params_update = {key:value for (key,value) in query_params_update.items()
                               if value is not None}                 
        query_params.update({key:value for key,value in iter(query_params_update.items())})               
        
        if query is not None:
            query_params[cls.QUERY_PARAM_KEYWORDS] = r"{}".format(query)
        query_string = urlparse.urlencode(query_params,doseq=True,quote_via=urlparse.quote_plus)
        search_url = f"{query_url}{query_string}"                                         
        
        if cls.DEBUG is True:              
            print("query params for update",query_params_update)
            print("updated query params",query_params)           
            print("search url",search_url)  
        return search_url   

    @classmethod    
    def get_query_url_iterator(cls,query=None,base=None,sort_by=None,sort_order=None,
                       search_type=None,search_forum=None,search_result=None,num_chars=None,days=None,
                       terms=None,author=None,start=0,num_steps=3,increment=15,member_list=False,active_topics=False):
        """constructs iterator returning 'num_steps' number of urls with increasing 'start' param starting with 'start', 
            increasing by 'increment' """  
        
        end = start + num_steps*increment
        start_indices = list(range(start,end,increment))
        query_urls = ( cls.get_query_url(query=query,base=base,
                                         sort_by=sort_by,sort_order=sort_order,search_type=search_type,
                                         search_forum=search_forum,search_result=search_result,num_chars=num_chars,
                                         days=days,terms=terms,author=author,start=start_index,member_list=member_list,
                                         active_topics=active_topics)                
                       for start_index in start_indices )
        return query_urls




        