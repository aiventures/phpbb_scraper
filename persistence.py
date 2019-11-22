""""Persistence module to store/access scraped data. So far, only a minimal json based persistence is implemented"""
import traceback
import json
import os
import shutil
from datetime import datetime

def read_json(filename, debug=False):
    """reads a given json file (UTF-8 format) from file system. Returns data as string"""

    # check if file exists
    if not os.path.isfile(filename):
        print(f"File {filename} not found")
        return None

    json_entries = []
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            json_entries = json.load(json_file)
    except:
        print("Exception opening file: ", filename)
        print(traceback.format_exc())
        json_entries = []

    if debug == True:
        print(f"File {filename} read, number of entries {len(json_entries)}")
    return json_entries

def append_json(filename, dict_entries, debug=False):
    """appends dictionary data to a json file as UTF-8 on file system 
       by reading file contents, deleting the old file and writing old content 
       with new content on a new file with the same file name
       opens file with 'w' (open as new or create)
    """

    if debug == True:
        print("Writing to File: ", filename)
        print("Adding Data / Num Entries:", str(len(dict_entries)))

    json_entries_out = []
    if os.path.isfile(filename):
        json_entries_out = read_json(filename)                
    
    [json_entries_out.append(json_entry) for json_entry in dict_entries]

    json_out = json.dumps(json_entries_out, indent=4, sort_keys=True, default=str)

    with open(filename, 'w', encoding='utf-8') as file:
        try:
            file.write(json_out)
        except:
            print(f"Exception writing file {filename}")
            print(traceback.format_exc())

def copy_file(source,target,force_delete=False):
    """ copies source to target file, in case target file exits, force_delete either
        will prevent copy or force a delete of previous file and copy of source file
    """ 
    if os.path.isfile(target):
        print(f"file {target} already exists, will be deleted {force_delete}")
        if force_delete is True:
            os.unlink(target)
        else:
            return
    shutil.copyfile(source,target)

def create_filename(filename,path=None,file_extension=None,append_timestamp=False):
    """ helper method to create a filename based on name, path , file extension and option
        to append a timestamp """

    if append_timestamp is True:              
        timestamp = "_"+datetime.now().strftime("%Y%m%d_%H%M%S")
    else:
        timestamp = ""    

    if file_extension is None:
        file_end = ""
    else:
        file_end = "." + file_extension
    
    if path is None:
        path_save = ""
    else:
        path_save = path+"\\"

    return path_save+filename+timestamp+file_end
    

def save_data(data,filename,path=None,file_extension=None,append_timestamp=False,encoding='utf-8'):
    """ saves data as string to file, optional with appended timestamp, returns path  """

    file_path = create_filename(filename,path=path,file_extension=file_extension,append_timestamp=append_timestamp)
    s = ""

    with open(file_path, 'w', encoding=encoding) as file:
        try:
            file.write(data)
            s = "Data saved to " + file_path
        except:
            print(f"Exception writing file {filename}")
            print(traceback.format_exc())     
            s = "No data was saved" 
            
    return s

def read_json_as_dict(filename, debug=False):
    """reads a given json file (UTF-8 format) from file system. Returns data as dictionary
       transform each json entry:
       {"<key>": "<value>",   "link": "<link>"} into dictionary entry
       {<key>:{"value":<value>,"link":<link>}}    
    """

    data_raw_entries = read_json(filename,debug=debug)
    if debug is True:
        print(f"read json as dict/1st File: Type {type(data_raw_entries[0])} \n {data_raw_entries[0]}")    
    entry_list = []
    for data_raw_entry in data_raw_entries:           
        attributes = json.loads(data_raw_entry)             
        attribute_dict = {}
        for attribute in attributes:            
            attribute_value = {}
            for k,v in attribute.items():
                if k != "link":            
                    key = k
                    value = v
                else:            
                    link = v
            attribute_value["value"] = value
            attribute_value["link"] = link
            attribute_dict[key] = attribute_value
        entry_list.append(attribute_dict)             
    return entry_list

def read_html_file_names(path,debug=False):
    """reads recursively html files from file directly"""

    file_paths = []
    for subpath,directories,files in os.walk(path):
        if debug is True:
            print(f"subpath \n {subpath} \n directories \n {directories} \n files \n {files} \n")
        for file in files:
            if '.htm' in file:            
                file_path = path+"\\"+file
                file_paths.append(file_path)
    return file_paths  
    
    
