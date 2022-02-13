'''
Use NER output to find a title, 
	use text to find answer to question.   
'''
import config
import datetime
import mysql.connector
from math import ceil

from transformers import AutoTokenizer
from transformers import AutoModelForTokenClassification
from transformers import pipeline


def find_ner_in_str(prompt):
    # use named entity recognition pipleline to source wikipedia context
    ner_pipe = pipeline("ner")
    ner_entity = prompt[ner_pipe(prompt)[0]['start']:ner_pipe(prompt)[-1]['end']]
    ner_entity_for_sql = ner_entity.replace(" ", "%") + '%'
    return ner_entity_for_sql

def get_idx_and_filename(ner_entity_for_sql: str):
    # Use NER output with sql title table to find idx from name
    query_1 = (
    	"SELECT * "
    	"FROM wiki_table "
    	f"WHERE title LIKE '{ner_entity_for_sql}' "
    	"ORDER BY LENGTH(title) ASC "
    	"LIMIT 1;"
    	)
    cursor.execute(query_1)
    # cursor hates being used as the list it is
    idx_in_list = [title_id for (title_id, title) in cursor]
    idx = idx_in_list[0]
    filename_number = ceil(idx / 10000)*10000
    return idx, filename_number

def get_text(idx, filename_number):
    # idx -> text from sql text table
    query_2 = (
    	"SELECT * "
    	f"FROM wiki_texts_{filename_number} "
    	f"WHERE title_id = '{idx}'; "
    	)
    cursor.execute(query_2)

    for (title_id, title, text) in cursor:
        return text

def get_soln(prompt, text):
    # use context to answer question via pipeline
    qa_pipe = pipeline("question-answering")
    result = qa_pipe(question=prompt, context=text)
    print(f"Answer: '{result['answer']}', \
            score: {round(result['score'], 4)}, \
            start: {result['start']}, end: {result['end']} "
            )

if __name__ == "__main__":
    cnx = mysql.connector.connect(user = config.user,
                                  passwd = config.passwd, 
                                  database='wiki')
    cursor = cnx.cursor()
    # prompt question to be answered
    prompt = input("Enter your question: ")
    # prompt = r"when was guillermo del toro born?"
    
    ner_entity_for_sql = find_ner_in_str(prompt)
    idx, filename_number = get_idx_and_filename(ner_entity_for_sql)
    text = get_text(idx, filename_number)
    get_soln(prompt, text) #print is in function

    cursor.close()
    cnx.close()