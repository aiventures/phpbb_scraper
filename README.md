#  PHPBB Scraper Library

## Introduction
This Python Lib will scrape PHPBB forum web pages. It will generate urls (or multiple arrays as well) for specific web pages such as topics only pages or pages with post texts. By means of a config file access to specific forums can be preconfigured. 
Scraped web pages (using Beautiful Soup) can be saved locally. From there, posts are analyzed (by means of RegEx) and statistics as python dictionaries be built up (for further analysis, for example number of posts per topic or access numbers, with dedicated Python libs such as Numpy :-) ).

All methods/functions can also be run in Debug mode to be able to figure out what the code is doing :-) 

## Limitations
Scraping might not work out of the box for every forum, so adaption to other forum layouts and other languages might be required.
Lib was only developed for Windows platform

## Structure
The scraper consists of the following python modules / Classes:
* `phpbb_scraper.scraper` - module to scrape contents from phpbb page also handles login into phpbb page
*  class `PhpbbScraper` in module phpbb_scraper.scraper - Class for scraping phpBB 
* `phpbb_scraper.soup_converter` - module to transform phpbb html code into beautiful soup objects
* `phpbb_scraper.html_converter` - utility module to transform data into html
* `phpbb_scraper.url_generator` - Class PhpbbUrlGenerator generates URL for reading phpbb web pages
*  class `PhpbbUrlGenerator` in module phpbb_scraper.url_generator: enerates URL for reading phpbb web pages
* `phpbb_scraper.persistence` - "Persistence module to store/access scraped data. So far, only a minimal json based persistence is implemented

## Usage Examples
A good way to check into functionality is the Jupyter Workbook `PHPBB_SCRAPER_HOWTO_PUBLIC.ipynb`, that explains in code how to use the different functions.
Documentation of all functions (as of November 2019) was copied to file `phpbb_scraper_api_doc.md` in `doc` folder

## Further help
Classes, functions, modules should be documented sufficiently. Use `dir(<module>)` or `help(<module>)` to get more information

## Any working samples?

Nope, won't publish specific data / forum posts

## Last Notice
**Act responsible** when scraping data ... meaning to be unobtrusive, nondestructive and respecting other people's privacy !

November 2019, aiventures
