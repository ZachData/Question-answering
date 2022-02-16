# Question-Answering Bot
Here, we use NER and question-answering pipelines for answering your questions based on Wikipedia's expansive texts. 

## Dataset

A MySQL database was built from a wikipedia dump. The official XML dump used to create the database can be found [here.](https://en.wikipedia.org/wiki/Wikipedia:Database_download)
Please torrent the files as opposed to downloading them directly, as this is easier on the server. The file should be around 50Gb in size.

The file cannot be directly imported into an SQL database, so the information must be harvested. I chose to collect the data into a CSV. Attempting to collect the data by simply looking at XML tags results in failure, so a special tool must be used: [WikiMedia's WMXML tool.](https://www.mediawiki.org/wiki/Mediawiki-utilities/mwxml) With this tool, creating the CSV which we can directly export as an SQL database is straightforward. 

I chose to limit the number of rows in each CSV containing the texts to 10^4 in order to keep filesize small (~200Mb). A simple bash script is provided in order to create tables and import the CSVs in a simple way. A 'master table' is produced in the python file which does not contain any of the entry's texts, only the titles and their appropriate index. This master table is not divided and contains all ~8 million Wikipedia entries.

For personal use, create a config.py file which contains all local paths, or replace config uses in your local files. 

## Model

NLP has never been easier thanks to HuggingFace. Using the Pipeline utility, we can quickly and effectively deploy popular, high-performing named-entity recognition (NER) and question-answering (QA) pretrained NLP models in very few lines. 

We use byte-pair encoding for both NER and QA. For NER we use a fine-tuned BERT model on CoNLL-2003, and for QA we use a fine-tuned BERT model on SQuAD. These are both the defaults for their respective tasks, and they are found to produce quite good results in very little time.
