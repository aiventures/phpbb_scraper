""" utility module to transform data into html """
def wrap(content,tag,lf=False):
    """embeds content string with html tags"""    
    if lf is False:
        return "<"+tag+">"+content+"</"+tag+">"    
    else:
        return "<"+tag+">\n"+content+"\n"+"</"+tag+">"    

def get_link(link,text):
    """gereates link"""
    return '<a href="'+link+'">'+text+'</a>'

def wrap_multiple(*items,tag="td",lf=False):    
    """wraps items in a list into html tags"""
    out = ""
    for __,item in enumerate(*items):    
        out += wrap(item,tag=tag,lf=lf)
        if lf is True:
            out += "\n"
    return out

def get_html_table(table_data):
    """creates  an html table, expects list of lists (rows and columns)"""

    html_out = ""
    if not type(table_data) is list:
        print("get_html_table, input is not a list")
        return None
    for row in table_data:
        if not type(row) is list:
            print("get_html_table, input line is not a list")
            return None
        html_cells = wrap_multiple(row,tag="td")
        html_line = wrap(html_cells,"tr",lf=False)
        html_out += html_line
    html_out = wrap(html_out,"table",lf=False)
    html_out = wrap(html_out,"html",lf=False)
    return html_out

def dict_with_key_as_html(topics_dict_list,debug=False):
    """ Generates HTML table for a list of dictionaries, extracts key values from 1st line. if a key has a corresponding key 
        with suffix _link, this entry will be treated as link (and value generated as url). If a key ends with url
        the value will also be treated as link.
        source dictionary is assumed of structure
        {keyX:{subkey1:valueX1,subkey2:valueX2,....},keyY:{subkey1:valueY1,subkey2:valueY2,....}} """

    post_list = []
    first_run = True
    counter = 1

    for key_topic in topics_dict_list:
        topic = topics_dict_list[key_topic]
        
        if first_run is True:
            first_run = False
            key_list = list(topic.keys())                    
        
        post_as_dict = {}        
        # add post unique hash id as post key
        post_as_dict['count'] = {'value':counter,'link':None}  
        post_as_dict['post_key'] = {'value':key_topic,'link':None}  
        counter += 1
        
        for key in key_list:                        
            # skip keys ending with link
            if key[-4:] == 'link':
                continue    
            #check if there is a a key with a link
            link = topic.get(key+'_link',None)
            value = topic.get(key,None)
            #use url if key end with url    
            if key[-3:] == 'url':
                link = value
            post_as_dict[key] = {'value':value,'link':link}  
        post_list.append(post_as_dict)    
        
    return dict_as_html(post_list)


def dict_as_html(dict_list,debug=False):
    """returns dictionary as html file. keys are header lines, data 
       is assumed of format <key>:{value:<value>,link:<link>}  """

    html_out = ""
    # assumption all keys are the same as first line of sata set
    keys = list(dict_list[0].keys())
    keys_html = wrap_multiple(keys)
    html_out += wrap(keys_html,tag="tr",lf=False)

    for row in dict_list:     
        values = []
        for key in keys:
            if row.get(key,None) is None:
                continue
            value =  str(row[key]["value"])
            link = row[key]["link"]
            if link is not None:
                value = get_link(link,value)
            values.append(value)
        values_html = wrap_multiple(values)
        html_out += wrap(values_html,tag="tr",lf=False)

    html_out = wrap(html_out,tag="table",lf=False)
    html_out = wrap(html_out,tag="html",lf=False)

    return html_out

def dict_as_html_simple(dict_list,debug=False):
    """returns dictionary as html file. keys are header lines, data 
      is assumed of format {<key>:<value>}  """
    dict_keys = list(dict_list[0].keys())
    html_dict_list = []
    for list_entry in dict_list:
        entry_list = {}
        for key in dict_keys:
            if list_entry.get(key,None) is None:
                continue
            value = list_entry[key]
            entry_list[key] = {"value":value,"link":None}            
        html_dict_list.append(entry_list) # use existing helper method
    return dict_as_html(html_dict_list,debug=debug)        