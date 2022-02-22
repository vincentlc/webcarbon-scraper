import re
import os
import csv
import requests
import pandas as pd

urls = open('urls.txt').readlines() # read all the url lines 
urls = [u.rstrip('\n').strip().rstrip('/').replace('https://', '').replace('http://', '').replace('www.', '') for u in urls] # parse the lines
urls = [u for u in urls if u]  # remove empties

def scrapeWebCarbon(url):
    '''
    Function takes a URL and scrapes the html to the disk, then extracts the grams of carbon from the HTML header.
    Returns a list
    '''
    carbonurl = 'https://www.websitecarbon.com'
    cleanurl = url.replace('.', '-').replace('/', '-')
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'wgd-cc-url':url,
               'wgd-cc-retest': 'true'}
    
    directory = 'html'
    if not os.path.exists(directory):
        os.makedirs(directory)
    if "?" in cleanurl:
        scrapefile = "./html/" + cleanurl.replace("?",'_' ) + ".html"
    else:
        # Make the request and save the response
        scrapefile = "./html/" + cleanurl + ".html"
    
    if not os.path.exists(scrapefile) or os.path.getsize(scrapefile) == 0:
        print('scraping ' + url)
        session = requests.Session()
        sess = session.post(carbonurl, headers=headers, data=payload)
        with open(scrapefile, "w") as f:
            f.write(sess.text)
            f.close()
    else:
        print('using cached html for ' + url)
        
    # Load the cached response file and search for the data
    # list of data to scrap
    data_list_search = {'"grams":': 17, '"litres":':18 , '"energy":':18, '"monthly_views":':25}
    result = [url]
    #search of data in file
    if os.path.exists(scrapefile):
        # opening a text file
        file1 = open(scrapefile, "r")
        # Loop through the file line by line
        for line in file1:  
            # checking string is present in line or not
            for data in data_list_search:
                if data in line:
                    value = line[data_list_search[data]:-2]
                    #print(value)
                    result.append(value)
                    #break 
        # closing text file    
        file1.close() 
    return result

carbondata = [scrapeWebCarbon(u) for u in urls]
print(carbondata)
with open('data_scrap_result.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['url', 'gram_c02', 'litres','energy', 'monthly_views'])
    writer.writerows(carbondata)

#Now you can multiply these values by your website pageviews analytics to calculate your website's carbon footprint.


