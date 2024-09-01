import pandas as p
import csv as c
import requests as r
import pymupdf
import hashlib as h
import time as t
import sys
from os.path import isfile,isdir
from os import mkdir
from unidecode import unidecode

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
                
                
            if not isfile(f"./txts/{pdf_filename}.txt"):
                
                doc = pymupdf.open(f"./pdfs/{pdf_filename}.pdf")
                out = open(f"./txts/{pdf_filename}.txt", "w")
                for page in doc:
                    out.write(page.get_text("text"))
                out.close()
            
            with open(f"./txts/{pdf_filename}.txt", "r") as f:
                full_text = f.read()
                full_text = unidecode(full_text)
                full_text = full_text.replace("\n", " ")
                full_text = full_text.replace("\r", " ")
                full_text = full_text.replace("\t", " ")
                full_text = full_text.replace("\f", " ")
                full_text = full_text.replace("\v", " ")
                full_text = full_text.replace("\b", " ")
                full_text = full_text.replace("\a", " ")
                full_text = full_text.replace("\e", " ")
                full_text = full_text.replace("\x0b", " ")
                full_text = full_text.replace("\x0c", " ")
                full_text = full_text.replace("\x0e", " ")
                full_text = full_text.replace("\x0f", " ")
                full_text = full_text.replace("\x10", " ")
                full_text = full_text.replace("\x11", " ")
                full_text = full_text.replace("\x12", " ")
                full_text = full_text.replace("\x13", " ")
                full_text = full_text.replace("\x14", " ")
                full_text = full_text.replace("\x15", " ")
                full_text = full_text.replace("\x16", " ")
                full_text = full_text.replace("\x17", " ")
                full_text = full_text.replace("\x18", " ")
                full_text = full_text.replace("\x19", " ")
                full_text = full_text.replace("\x1a", " ")
                full_text = full_text.replace("\x1b", " ")
                full_text = full_text.replace("\x1c", " ")
                full_text = full_text.replace("\x1d", " ")
                full_text = full_text.replace("\x1e", " ")
                full_text = full_text.replace("\x1f", " ")
                full_text = full_text.replace("\x7f", " ")
                full_text = full_text.replace("\x80", " ")
                full_text = full_text.replace("\x81", " ")
                full_text = full_text.replace("\x82", " ")
                full_text = full_text.replace("\x83", " ")
                full_text = full_text.replace("\x84", " ")
                full_text = full_text.replace("\x85", " ")
                full_text = full_text.replace("\x86", " ")
                full_text = full_text.replace("\x87", " ")
            
            record["fulltext"] = full_text
                
            records.append(record)
        except:
            print(count, "[PDF ERROR]", pdf_filename, row.url, sys.exc_info())
            count = count - 1
            error_count = error_count + 1

            

    header = ["category", "fulltext"]
    # create csv
    with open(f"./../data/data.csv", 'w') as f:
        writer=c.writer(f, delimiter=',', dialect='unix')
        writer.writerow(header)
    
        for row in records:
            writer.writerow([row["category"], row["fulltext"]])
    
    records = []

    print(lang, "total records:", line_count, "/ failed records:", error_count, "/ skipped records:", skip_count, "/ processed records:", count)

if __name__ == "__main__":

    urllist = "scraped_urls1.xlsx"
    print(f"processing {urllist}")
    processor(urllist)

