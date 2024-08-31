import pandas as p
import csv as c
import requests as r
import pymupdf
import hashlib as h
import time as t
import sys
from os.path import isfile,isdir
from os import mkdir

chunk_size = 1024*10

values = {}

def processor(lang):
    maindf = p.read_excel(lang, engine="openpyxl")
    records = []
    count = 0
    error_count = 0
    line_count = 0
    skip_count = 0
    
    for row in maindf.itertuples():
        count = count + 1
        line_count = line_count + 1

        record = {}

        url = row.url

        pdf_filename = (h.sha1(((row.url).split("#page=")[0]).encode())).hexdigest()
        record["category"] = row.category

        if isfile(f"./pdfs/{pdf_filename}.pdf"):
            pass
        else:
            print(f"downloading {url}")
            res = r.get(row.url, stream=True)
            if res.status_code != 200:
                print(count, "[URL ERROR]", res.status_code, row.url)
                count = count - 1
                error_count = error_count + 1
                
            elif res.status_code == 200:
                with open(f"./pdfs/{pdf_filename}.pdf", "wb") as wfp:
                    for chunk in res.iter_content(chunk_size):
                        wfp.write(chunk)
            
        try:
            full_text = ""
                
                
            if not isfile(f"./pdfs/txts/{pdf_filename}.txt"):
                
                doc = pymupdf.open(f"./pdfs/{pdf_filename}.pdf")
                out = open(f"./pdfs/txts/{pdf_filename}.txt", "wb")
                for page in doc:
                    full_text = page.get_text("text").encode("utf8")
                    out.write(full_text)
                    out.write(bytes((12,)))
                out.close()
            else:
                
                doc = pymupdf.open(f"./pdfs/txts/{pdf_filename}.txt")
                for page in doc:
                    full_text = page.get_text("text").encode("utf8")
                
            
            record["fulltext"] = full_text
                
            records.append(record)
        except:
            print(count, "[PDF ERROR]", pdf_filename, row.url, sys.exc_info())
            count = count - 1
            error_count = error_count + 1

            

    header = ["category", "fulltext"]
    # create csv
    with open(f"./jsons/{lang}.json", 'w') as f:
        writer=c.writer(f, delimiter=',', lineterminator='\n', dialect='unix')
        writer.writerow(header)
    
        for row in records:
            writer.writerow([row["category"], row["fulltext"]])
    
    records = []

    print(lang, "total records:", line_count, "/ failed records:", error_count, "/ skipped records:", skip_count, "/ processed records:", count)

if __name__ == "__main__":

    urllist = "scraped_urls.xlsx"
    print(f"processing {urllist}")
    processor(urllist)

