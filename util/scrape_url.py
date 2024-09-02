import requests
from bs4 import BeautifulSoup
import ssl
import warnings
from openpyxl import Workbook
import csv as csv

import requests.packages.urllib3.exceptions as urllib3_exceptions

warnings.simplefilter("ignore", urllib3_exceptions.InsecureRequestWarning)

def extract_url(sourceurl, category):

    records = []
     
    class TLSAdapter(requests.adapters.HTTPAdapter):
        def init_poolmanager(self, *args, **kwargs):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.set_ciphers("DEFAULT@SECLEVEL=1")
            ctx.options |= 0x4
            kwargs["ssl_context"] = ctx
            return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


    

    with requests.session() as s:
        s.mount("https://", TLSAdapter())

        response = s.get(sourceurl)
        soup = BeautifulSoup(response.text, 'html.parser')

        urls = []

        # xlsfilename
        #xlsfilename = 'scrape_full.xlsx'
        
        # open workbook
        #wb = Workbook(xlsfilename)

        #ws = wb.index
        
        #ws = wb.active
        #row = ['test1', 'test2']
        #ws.append(row)
        # grab active worksheet
        #sheet = wb.active
        #sheet.append(["test", "two"])

        
        
                       

        for link in soup.table.find_all('a'):
            url = ''
            record = {}
            
            # check first character of string link
            if link.get('href')[0] == '/' :
                #print("https://policy.un.org" + link.get('href'))
                url = "https://policy.un.org" + link.get('href')
            else:
	            #print(link.get('href'))
                #url = link.get('href')
                if link.get('href').find("https://www.undocs.org/en/") > -1 :
                    url = link.get('href')
                elif link.get('href').find("https://www.undocs.org/") > -1 :
                    url = link.get('href').replace("https://www.undocs.org/", "https://www.undocs.org/en/")
                else:
                    url = link.get('href')

            record["url"] = url
            record["category"] = category

            records.append(record)

        with open(f"scrapefull.csv", 'a') as f:
            writer=csv.writer(f, delimiter=',', dialect='unix')
            for row in records:
                writer.writerow([row["url"], row["category"]])

        records = []
            
            

        #wb.save(xlsfilename)

if __name__ == "__main__":
    
    sourceurls = ["https://policy.un.org/policy-all?f%5B0%5D=node%253Afield_document_topic_theme%253Aparents_all%3A30425", "https://policy.un.org/policy-all?f%5B0%5D=node%253Afield_document_topic_theme%253Aparents_all%3A30425&page=1"]
    sourcecategories = ["accountability", "accountability"]

    with open(f"scrapefull.csv", 'w') as f:
        writer=csv.writer(f, delimiter=',', dialect='unix')
        writer.writerow(["url", "category"])
    f.close()

    for sourceurl, sourcecategory in zip(sourceurls, sourcecategories):
        print(f"processing {sourceurl} - {sourcecategory}")
        extract_url(sourceurl, sourcecategory)
    

