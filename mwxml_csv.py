'''
Wikipedia parsing tool. XML -> CSV.
Text is large (~10^6 bytes), and will be put into its own csv with id. 
Other info will be put into a csv as well, to be loaded into MySQL server. 
'''

import mwxml
import glob
import os
import re
import unidecode
import pandas as pd
import config

os.chdir(r'/home/zach/Desktop/Datasets/Wiki/')
pathWikiXML = os.path.join(config.PATH_WIKI_XML, config.FILENAME_WIKI)
paths = glob.glob(pathWikiXML)

def process_dump(dump, path):
    for page in dump:
        for revision in page:
            if revision.text is not None and len(revision.text) > 1000:
                text = text_cleaner(revision.text)
                text = text_shortener(text)
                # print(repr(text))
                yield page.id, page.title, repr(text)

def text_cleaner(text):
    #remove all accents
    text = unidecode.unidecode(text)

    # remove all undesired characters
    text = re.sub(' +', ' ', text)
    text = re.sub('\n', '', text)
    text = re.sub('[\|\}\{\[\]\=\*<>()]', '', text)
    text = re.sub(r'(\s\w+[.,?!"])+\S+', r'\1', text) # 'strong.sfnFiala2017loc"4' -> 'strong.'
    return text

def text_shortener(text):
    # stop reading after 'see also', if it exists
    stop_signal = text.find('See also')
    if stop_signal != -1:
        text = text[0: stop_signal]
    return text

    
def main():
    # take stream of large data, make into managable csv files
    counter = 1
    data_text = []
    data_not_text = []
    for page_id, page_title, text in mwxml.map(process_dump, paths):
        data_text.append([counter, page_title, text])
        data_not_text.append([counter, page_title])
        counter += 1
        
        if counter % 10000 == 0:
            print(counter)
            # list -> pandas df
            df_text = pd.DataFrame(data_text, 
                        columns=['index', 'title', 'text']
                        )
            # reset list
            data_text = []
            # pandas df -> csv
            df_text.to_csv(f'wiki_text_csvs/wiki_texts_{counter}.csv', 
                           index=False,
                           sep='|'
                           )
 
    # save master list at end of file
    df_not_text = pd.DataFrame(data_not_text, 
                    columns=['index', 'title']
                    )
    df_not_text.to_csv(f'wiki_no_text_csvs/wiki_data_{counter}.csv', 
                       index=False,
                       )

if __name__ == '__main__':
    main()


