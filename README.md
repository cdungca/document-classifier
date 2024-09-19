# Document Classifier: Initial Report and Exploratory Data Analysis

The aim of this study is to identify a model which will accurately predict the category of a specific document. Currently, the task of categorizing is done manually by a person upon uploading the document to the site. Automating this process will allow the person to focus more on strategic activities and this can also be used and scale for other document classification tasks. 

The documents for classification are taken from the UN website, called [Policy Portal](https://policy.un.org). You can follow the analysis in the [Jupyter notebook](https://github.com/cdungca/document-classifier/blob/main/main.ipynb).

## Data Collection and Preparation
To extract the documents with their corresponding label/category, we will first scrape the links in the [Search Portal](https://policy.un.org/policy-all) page. Once we've collected the urls, we will extract the full text on those pdf documents and store them in a csv file with their corresponding label. 

We can then load the data perform data cleaning and preparation. Here are the high level steps for the cleaning/preparation:

1. Remove rows with null values
2. Change all texts to lower case
3. Perform tokenization
4. Remove stop words 
5. Remove non alphabetic texts
6. Apply word lemmatizatiom

## Data Analysis

After loading the data, here is a breakdown of the number of documents per category:

|Category|Number of Documents|
|--------|-------------------|
|Travel|75|
|Human Resources|66|
|Accountability|42|
|Health and Wellbeing|11|

![alt text](https://github.com/cdungca/document-classifier/blob/main/images/category_distribution_before_cleaning.png "Category Distribution")

As we can see, we have an imbalance data set and there are too few documents for Health and Wellbeing. We will remove those documents and do the analysis with 3 categories. Here's the distribution after cleaning the data:

![alt text](https://github.com/cdungca/document-classifier/blob/main/images/category_distribution_after_cleaning.png "Final Data Set")

Here are representations of the words found in each category:

Travel:
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/wordcloud_travel.png "Travel Word Cloud")

Human Resources:
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/wordcloud_hr.png "Human Resources Word Cloud")

Accountability:
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/wordcloud_accountability.png "Accountability Word Cloud")


## Modeling

To find the best model for our objective, we will be looking at accuracy as a measure in comparing the different models, feature extraction techniques, and hyperparameters.

We will be using DummyClassifier as our baseline model. The accuracy for our baseline model is **38.46%**.

Here are the results using different combinations of model, feature extraction (CountVectorizer and TfidVectorizer), default, and best parameters

### Bag-of-words using CountVectorizer

#### 1. CountVectorizer - Logical Regression - Default Parameters - Accuracy => **55.77%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_cvect_lgr_default.png "Bag-of-words: Confusion Matrix: Logistic Regression - Default Parameters")
#### 2. CountVectorizer - Logical Regression - Best Parameters - Accuracy => **59.62%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_cvect_lgr_best.png "Bag-of-words: Confusion Matrix: Logistic Regression - Best Parameters")
#### 3. CountVectorizer - Naive Bayes - Default Parameters - Accuracy => **76.92%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_cvect_nb_default.png "Bag-of-words: Confusion Matrix: Naive Bayes - Default Parameters")
#### 4. CountVectorizer - Naive Bayes - Best Parameters - Accuracy => **76.92%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_cvect_nb_best.png "Bag-of-words: Confusion Matrix: Naive Bayes - Best Parameters")
#### 5. CountVectorizer - Support Vector Machine - Default Parameters - Accuracy => **50%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_cvect_svm_default.png "Bag-of-words: Confusion Matrix: Support Vector Machine - Default Parameters")
#### 6. CountVectorizer - Support Vector Machine - Best Parameters - Accuracy => **69.23%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_cvect_svm_best.png "Bag-of-words: Confusion Matrix: Support Vector Machine - Best Parameters")

### TF-IDF using TfidVectorizer

#### 1. TfidVectorizer - Logical Regression - Default Parameters - Accuracy => **75%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_tvect_lgr_default.png "TF-IDF: Confusion Matrix: Logistic Regression - Default Parameters")
#### 2. TfidVectorizer - Logical Regression - Best Parameters - Accuracy => **71.15%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_tvect_lgr_best.png "TF-IDF: Confusion Matrix: Logistic Regression - Best Parameters")
#### 3. TfidVectorizer - Naive Bayes - Default Parameters - Accuracy => **80.77%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_tvect_nb_default.png "TF-IDF: Confusion Matrix: Naive Bayes - Default Parameters")
#### 4. TfidVectorizer - Naive Bayes - Best Parameters - Accuracy => **76.92%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_tvect_nb_best.png "TF-IDF: Confusion Matrix: Naive Bayes - Best Parameters")
#### 5. TfidVectorizer - Support Vector Machine - Default Parameters - Accuracy => **50%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_tvect_svm_default.png "TF-IDF: Confusion Matrix: Support Vector Machine - Default Parameters")
#### 6. TfidVectorizer - Support Vector Machine - Best Parameters - Accuracy => **76.92%**
![alt text](https://github.com/cdungca/document-classifier/blob/main/images/cm_tvect_svm_best.png "TF-IDF: Confusion Matrix: Support Vector Machine - Best Parameters")

Here's a summary of the accuracy on unseen/test data:

|Model Combination|Test Accuracy|
|-----------------|-------------|
|CountVectorizer - Logical Regression - Default Parameters|55.77|
|CountVectorizer - Logical Regression - Best Parameters|59.62|
|CountVectorizer - Naive Bayes - Default Parameters|76.92|
|CountVectorizer - Naive Bayes - Best Parameters|55.77|
|CountVectorizer - Support Vector Machine - Default Parameters|50|
|CountVectorizer - Support Vector Machine - Best Parameters|69.23|
|TfidVectorizer - Logical Regression - Default Parameters|75|
|TfidVectorizer - Logical Regression - Best Parameters|71.15|
|TfidVectorizer - Naive Bayes - Default Parameters|**80.77**|
|TfidVectorizer - Naive Bayes - Best Parameters|76.92|
|TfidVectorizer - Support Vector Machine - Default Parameters|50|
|TfidVectorizer - Support Vector Machine - Best Parameters|76.92|

In general, TF-IDF performs better than bag-or-words in our use case. The highest accuracy of 80.77% is achieved with TF-IDF, Naive Bayes, and default parameters. Here's the classification report for that model:

||Precision|Recall|F1-score|Support|
|--|--|--|--|--|
|Accountability|0.77|0.83|0.80|12|
|Human Resources|0.75|0.75|0.75|20|
|Travel|0.89|0.85|0.87|20|
| | | | | |
|Accuracy| | |0.81|52|
|Macro Avg|0.80|0.81|0.81|52|
|Weighted Avg|0.81|0.81|0.81|52|

The model has the highest accuracy of **89%** when predicting documents categorized as Travel. The classes in our dataset are relatively balanced since macro and weighted average are almost the same.







