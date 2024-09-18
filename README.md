# Document Classifier: Initial Report and Exploratory Data Analysis
The aim of this study is to identify a model which will accurately predict the category of a specific document. Currently, the task of categorizing is done manually by a person when a document is uploaded in the site. Automating this process will allow the person to focus more on strategic activities and also scale it to other document classification tasks. 

The documents for training and testing are taken from a UN public website, called Policy Portal. For this study, we will limit the scope and use approximately 300 documents. You can follow the analysis in the Jupyter notebook.

## Data Collection and Preparation
To extract the documents with their corresponding label/category, we will scrape the links in the Search Portal page. Once we've identified the urls, we will extract the full text on those pdf documents and store them in a csv file together with their label. 

Once we have the category and full text in a csv, we can load them in our script and perform and perform data cleaning an preparation. Here are the steps for the preparation:

1. Remove rows with null values
2. Change all text to lower case
3. Perform tokenization
4. Remove stop words 
5. Remove non alphabetic texts
6. Apply word lemmatizatiom

## Data Analysis
After scraping and cleaning the data, here is a breakdown of the number of documents per category:

## Modeling

